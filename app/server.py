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
from rag import get_retriever, format_docs
from incidence_model import Llm
from qa_model import QaLlm

app = FastAPI(
    title="Server chat",
    version="1.0",
    description="Simple api server to chat with a model"
)  

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

qa = QaLlm()

add_routes(
    app,
    qa.chain(),
    path="/chat",
)

llm = Llm()

# Chain que resolverá las incidencias automáticamente
add_routes(
    app,
    llm.chain(),
    path="/incidence",
)

# Edit this to add the chain you want to add
#add_routes(app, NotImplemented)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
