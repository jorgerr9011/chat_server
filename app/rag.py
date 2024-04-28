from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from data import write_data

def get_retriever():
    
    write_data()
    
    loader = JSONLoader(
            file_path="./registros/data.json",
            jq_schema='.',
            is_content_key_jq_parsable=True,
            text_content=False
        ).load()
    
    text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=1000, chunk_overlap=200, length_function=len, is_separator_regex=False)
    texts = text_splitter.split_documents(loader)

    embeddings = OllamaEmbeddings(base_url='http://localhost:11434', model="mistral")
    db = FAISS.from_documents(texts, embeddings)

    return db.as_retriever()

def format_docs(docs):
     return "\n\n".join(doc.page_content for doc in docs)
