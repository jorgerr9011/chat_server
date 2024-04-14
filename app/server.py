from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_community.document_loaders.mongodb import MongodbLoader
from langchain_community.vectorstores import FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_text_splitters import CharacterTextSplitter

from langchain.chains.query_constructor.base import (StructuredQueryOutputParser, get_query_constructor_prompt)
import json
from pathlib import Path
from data import write_data

app = FastAPI(
    title="Server chat",
    version="1.0",
    description="Simple api server to chat with a model"
)  

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


ollama = Ollama(base_url='http://localhost:11434', model="mistral")
output_parser = StrOutputParser()

def format_docs(docs):
     return "\n\n".join(doc.page_content for doc in docs)

retriever = get_retriever()

# contextualize_system_prompt = """Given a chat history and the latest user question which might reference context in the chat history, formulate /
# a standalone question which can be understood without the chat history. Do not answer the question, just reformulate it if needed and /
# otherwise return it as is."""
template = """You are a technical support specialist in an IT department who are specialized in resolve incidences, answer queries and provide assistance. /
Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't /
try to make up an answer. If you don't find any relevant information to the question, don't talk about it and just say "Sorry I can't help you with that".

{context}

Question: {input}

Answer:"""

custom_rag_prompt = PromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever, "input": RunnablePassthrough()}
    | custom_rag_prompt
    | ollama
    | StrOutputParser()
)

# contextualize_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", contextualize_system_prompt),
#         MessagesPlaceholder(variable_name="chat_history"),
#         ("human", "{input}")
#     ]
# )

#history_aware_retriever = create_history_aware_retriever(ollama, retriever, contextualize_prompt)
#history_aware_retriver = (contextualize_prompt | ollama | StrOutputParser()).with_config(tags=["contextualize_prompt"])

#TEMPLATE = """You are a technical support specialist in an IT department who are specialized in resolve incidences, answer queries and provide assistance. /
#Current conversation: 
#{chat_history} 
            
#User: {input}
#AI:"""

# TEMPLATE = """You are a technical support specialist in an IT department who are specialized in resolve incidences, answer queries and provide assistance. /

# {context}"""

# qa_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", TEMPLATE),
#         MessagesPlaceholder(variable_name="chat_history"),
#         ("human", "{input}"),
#     ]
# )

# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# def contextualized_question(entrada: dict):
#     if entrada.get("chat_history"):
#         return history_aware_retriver
#     else:
#         return entrada["input"]

# rag_chain = (
#     RunnablePassthrough.assign(context=contextualize_prompt | retriever)
#     | qa_prompt
#     | ollama
# )

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

add_routes(
    app,
    rag_chain,
    path="/chat",
)

# Edit this to add the chain you want to add
#add_routes(app, NotImplemented)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
