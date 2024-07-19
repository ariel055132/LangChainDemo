from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

import constants


# a function for fetching embeddings in chroma db
def fetch_embeddings():
    collection = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())
    print(collection.get().keys())
    embeddings = collection.get(include=["embeddings"])
    return embeddings


# Load data from vector database.

CHROMA_PATH = constants.CHROMA_BIAN_PATH

load_dotenv('config.env')
print(os.environ.get('OPENAI_API_KEY'))

vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())
#embeddings = fetch_embeddings()
# print(embeddings)
# {'ids': [], 'embeddings': None, 'documents': [], 'metadatas': []}
print(vectordb.get())
