import csv
import shutil
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import openai
import constants

load_dotenv('config.env')
openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = constants.CHROMA_BIAN_PATH
FILE_PATH = constants.FILE_PATH

# Define the columns we want to embed vs which ones we want in metadata
columns_to_embed = ["Service Domain", "Role Definition"]
columns_to_metadata = ["Service Domain", "Business Area", "Business Domain", "functionalPattern", "assetType",
                       "genericArtefactType", "Examples Of Use", "Role Definition"]

# Process the CSV into the embedable content vs the metadata and put it into Document format so that we can chunk it into pieces.
docs = []
with open('data/files/BIAN v12 asset(SD).csv', newline="", encoding='utf-8-sig') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for i, row in enumerate(csv_reader):
        to_metadata = {col: row[col] for col in columns_to_metadata if col in row}
        values_to_embed = {k: row[k] for k in columns_to_embed if k in row}
        to_embed = "\n".join(f"{k.strip()}: {v.strip()}" for k, v in values_to_embed.items())
        newDoc = Document(page_content=to_embed, metadata=to_metadata)
        docs.append(newDoc)

# Split the document using Chracter splitting.
splitter = CharacterTextSplitter(separator="\n",
                                 chunk_size=600,
                                 chunk_overlap=0,
                                 length_function=len)
documents = splitter.split_documents(docs)
print(documents)

# Generate embeddings from documents and store in a vector database
embeddings_model = OpenAIEmbeddings()
if os.path.exists(CHROMA_PATH):
    shutil.rmtree(CHROMA_PATH)

db = Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory=CHROMA_PATH)
db.persist()
