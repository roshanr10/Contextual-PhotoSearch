# Contextual PhotoSearch
Roshan Ravi <<roshan@roshanravi.com>> – NYC AI Hackathon - August 26th 2023

# Motivation
As a photographer, I take lots of photos for fun with friends/family, on my own to sharpen my craft, and at events for other people/organizations. In the past 12 months, this has resulted in close to 50,000 photos, not including my phone camera roll.


However, it is difficult to find images quickly, especially when trying to find a former photo to show my style to photographers I partner with to coordinate styles, like:

- "shot of the Statue of Liberty from Brooklyn"
- "graduation photos overlooking the river with a backdrop of New York City"
- "low light event photography of people hanging out"

these are all shots I  searched for during a convo with an old friend on Friday, August 25th 2023).


Despite Adobe Lightroom/Apple Photos/Google Photos having basic search capabilities, they appear to operate primarily based on keyword(s) searching, and choke on more complex scenarios, or do not generalize a complex query well enough to get an expected hit. Contextual PhotoSearch takes your query, enhances it using Cohere's LLM, then queries it against MongoDB's Atlas Vector Search to return scored image matches.

As an additional benefit, this could potentially also lead to more accessible photography platforms to search by autogenerating captions for those that may not already have one and enable searching atop them.

# Overview
## Step 1: load.py
This runs image-to-text translation on all images in the `./images` folder, embeds the resultant text using Cohere embeddings via LangChain, and then loads into a MongoDB Atlas cluster w/ a Vector Search index atop the embeddings.

## Step 2(a): search.py
The search script demonstrates the query ability by converting a text input into a MongoDB query using the Cohere LangChain integration, and returns the image metadata.

## Step 2(b): chat.py
This builds atop the search query to develop a more rebust query using Cohere's LLM via a LangChain LLMChain.

# Output
chat.py exports the text description and path to images for the top 2 hits based on the similarity score

## Potential Next Steps
- Introduce an image store alongside the metadata/embeddings
- Add a NextJS web UI to streamline usage for image upload & search
    - Enable user correction of 
- Include image EXIF metadata as part of searchable information, via context (i.e. high ISO likely implies low light)
- Summarize entire albums for searchability & providing accessible captions

# Photos
All photos were taken by Roshan Ravi.
