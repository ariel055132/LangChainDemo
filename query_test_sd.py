import argparse
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import openai
import constants

'''
Query Test for finding service domain of BIAN framework.
'''

load_dotenv('config.env')
openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = constants.CHROMA_BIAN_PATH

# Prepare the DB.
embedding_function = OpenAIEmbeddings()
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

query = "How to set up contract of new employee"
docs = db.similarity_search(query, k=3)
#docs = db.similarity_search_with_score(query)
#print('Retrieved docs:', docs)
for doc in docs:
    print(doc.page_content)
    print(doc.metadata)
    print("-" * 40)