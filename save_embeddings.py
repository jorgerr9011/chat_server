from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import JSONLoader

import chromadb
import os

def save_embeddings(persist_directory: str = "db"):

        loader = JSONLoader(
            file_path="./registros/prueba.json",
            jq_schema='.pages[]',
            is_content_key_jq_parsable=True,
            text_content=False
        ).load()

        text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=1000, chunk_overlap=200, length_function=len, is_separator_regex=False)
        documents = text_splitter.split_documents(loader)

        Chroma.from_documents(documents, OllamaEmbeddings(model="mistral"), persist_directory=persist_directory)

        my_db = Chroma(persist_directory=persist_directory, embedding_function=OllamaEmbeddings(model="mistral"))
        print(my_db._client.get_collection("langchain").get()['ids'])

        print("Finish")

        # retriever = db.as_retriever()
        #return db.as_retriever()


def delete_db(persist_directory):

    my_db = Chroma(persist_directory=persist_directory, embedding_function=OllamaEmbeddings(model="mistral"))

    for collection in my_db._client.list_collections():
        ids = collection.get()['ids']
        print('REMOVE %s document(s) from %s collection' % (str(len(ids)), collection.name))
        if len(ids): collection.delete(ids)
    
    print(my_db._client.list_collections())
    

def main():

    print("Starting")

    persist_directory = "./db"

    # Quizás aquí tengo que procesar un poco más como meto los documentos

    try: 
        #delete_db(persist_directory)
        save_embeddings(persist_directory)

    except Exception as e:
        print("Error guardando embeddings", e)


if __name__ == "__main__":

    main()

    