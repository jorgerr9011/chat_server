from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI(
    title="Server chat",
    version="1.0",
    description="Simple api server to chat with a model"
)    

class modelo :
    
    def __init__(self):
        
        TEMPLATE = """You are a technical support specialist who are specialized in resolve issues, answer queries and provide assistance. /
        Current conversation: 
        {chat_history} 
        
        User: {input}
        AI:"""

        ollama = Ollama(base_url='http://localhost:11434', model="mistral")

        prompt = ChatPromptTemplate.from_template(TEMPLATE)
        output_parser = StrOutputParser()

    def get_chain(self):

        return self.prompt | self.ollama
    
    def get_embeddings(self, text: str):
        return "fdjs"


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


add_routes(
    app,
    modelo.get_chain(),
    path="/chat",
)

add_routes(
    app,
    Ollama(base_url='http://localhost:11434', model="mistral"),
    path="/mistral"
)

# Edit this to add the chain you want to add
#add_routes(app, NotImplemented)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
