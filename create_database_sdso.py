import csv
import shutil
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import openai
from langchain_text_splitters import RecursiveCharacterTextSplitter

import constants

load_dotenv('config.env')
openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = constants.CHROMA_BIAN_SD_SO_PATH
FILE_PATH = constants.FILE_PATH

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    #print(chunks)
    #save_to_chroma(chunks)

def load_documents():
    #loader = DirectoryLoader(DATA_PATH, glob="*.md")
    loader = DirectoryLoader(FILE_PATH, glob="*.csv")
    documents = loader.load()
    print(documents)
    return documents


def split_text(documents: list[Document]):
    splitter = CharacterTextSplitter(separator="\n",
                                     chunk_size=600,
                                     chunk_overlap=0,
                                     length_function=len)
    chunks = splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()