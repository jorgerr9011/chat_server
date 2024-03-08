from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import JSONLoader

import os

class SearchIncidence():

    def __init__(self) -> None:

        persist_directory = "db"
        embedding = OllamaEmbeddings(model="mistral")

        if not os.path.exists('db'):
            print("No database found")
            raise Exception("No database found")
        
        self.vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    
    def SearchIncidence(self, query: str = None):

        results = self.vectordb.similarity_search_with_score(query, k=1)

        return results