from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
#from .qa_model import QaLlm
from .incidence_model import Llm
from .qa_history import LlmChatHistory

app = FastAPI(
    title="Server chat",
    version="1.0",
    description="Simple api server to chat with a model"
)  

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

#qa = QaLlm()

#add_routes(
 #   app,
  #  qa.chain(),
   # path="/chat",
#)

llm = Llm()

# Chain que resolverá las incidencias automáticamente
add_routes(
    app,
    llm.chain(),
    path="/incidence",
)

llmChat = LlmChatHistory()

add_routes(
    app, 
    llmChat.chain(),
    path="/chat"
)

# Edit this to add the chain you want to add
#add_routes(app, NotImplemented)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
