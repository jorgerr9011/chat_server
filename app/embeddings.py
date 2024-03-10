from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import JSONLoader

from langchain.chains.question_answering import load_qa_chain
from langchain.chains import (RetrievalQA, LLMChain, ConversationalRetrievalChain) 
import os

class Search_incidence():

    def __init__(self):

        persist_directory = "db"
        embedding = OllamaEmbeddings(model="mistral")
        if not os.path.exists('db'):
            print("No database")
            raise Exception("No database")
        
        print("Cargando db")
        self.vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    def incidence(self, modelo,text: str = None):
        retriever = self.vectordb.as_retriever()

        return RetrievalQA.from_llm(modelo, retriever=retriever)

        



