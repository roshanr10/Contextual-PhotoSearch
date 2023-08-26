from pathlib import Path
import hashlib

import pymongo
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from langchain.embeddings import CohereEmbeddings

def load_image(image_path):
    image_raw = Image.open(image_path).convert('RGB')

    return {
        "path": image_path,
        "raw": image_raw,
        "hash": hashlib.sha256(image_raw.tobytes()).hexdigest(),
        "tensor": None,
        "text": None,
        "embeddings": None
    }

blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
def image_to_metadata(image):
    image["tensor"] = blip_model.generate(
        **blip_processor(image["raw"], return_tensors="pt"),
        max_new_tokens=100
    )
    image["text"] = blip_processor.decode(image["tensor"][0], skip_special_tokens=True)
    
    return image

cohere_embedder = CohereEmbeddings(cohere_api_key="<COHERE API KEY>", model="embed-english-light-v2.0") # TODO REMOVE
def metadata_to_embeddings(images):
    return cohere_embedder.embed_documents([image["text"] for image in images], )

def embed_embeddings(image_metadata, image_embedding):
    image_metadata["embeddings"] = image_embedding
    return image_metadata

def to_document(image):
    return {
        "_id": str(image["hash"]),
        "path": str(image["path"]),
        "text": str(image["text"]),
        "embeddings": image["embeddings"]
    }

client = pymongo.MongoClient(
    '<CONNECTION STRING>',
    tls=True,
    tlsCertificateKeyFile='./mdb-client-cert.pem'
)

if __name__ == '__main__':
    images = [load_image(image_path) for image_path in Path("images").glob('*.jpg')]
    images_metadata = [image_to_metadata(image) for image in images]
    # print(images_metadata)

    images_embeddings = metadata_to_embeddings(images_metadata)
    # print(images_embeddings)

    images_metadata = [embed_embeddings(image_metadata, images_embeddings[image_index]) for (image_index, image_metadata) in enumerate(images_metadata)]
    # print(images_metadata)

    images_documents = [to_document(image) for image in images]
    # print(images_documents)

    client["photos"]["metadata"].bulk_write([
        pymongo.UpdateOne(
            { "_id": document["_id"] },
            { "$set": document },
            upsert=True
        ) for document in images_documents
    ])
