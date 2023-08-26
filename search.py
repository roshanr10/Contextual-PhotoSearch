import pymongo
from langchain.embeddings import CohereEmbeddings

cohere_embedder = CohereEmbeddings(cohere_api_key="<COHERE API KEY>", model="embed-english-light-v2.0") # TODO REMOVE

client = pymongo.MongoClient(
    '<CONNECTION STRING>',
    tls=True,
    tlsCertificateKeyFile='./mdb-client-cert.pem'
)

def query(text, k=2, embed_function=cohere_embedder.embed_query):
    return client["photos"]["metadata"].aggregate([
        {
            "$search": {
                "index": "default",
                "knnBeta": {
                    "vector": embed_function(text),
                    "path": "embeddings",
                    "k": k,
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "path": 1,
                "text": 1,
                "score": { "$meta": "searchScore" }
            }
        }
    ])

def print_result(results):
    print([doc for doc in results])
    print("--")

if __name__ == '__main__':
    print_result(query("people playing pool"))
    print_result(query("people hanging out at a bar"))
