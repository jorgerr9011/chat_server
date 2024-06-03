from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from .rag import get_retriever, format_docs

class Llm:

    template = """You are a technical support specialist in an IT department who are specialized in resolve incidences, answer queries and provide assistance. /
        Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't /
        try to make up an answer. If you don't find any relevant information to the question, don't talk about it and just say "Sorry I can't help you with that".
        {context}

        Question: {input}
        
        Answer:"""

    custom_rag_prompt = PromptTemplate.from_template(template)

    ollama = Ollama(base_url='http://localhost:11434', model="mistral")
    output_parser = StrOutputParser()
        

    def chain(self):
        
        retriever = get_retriever()

        rag_chain = (
            {"context": retriever, "input": RunnablePassthrough()}
            | self.custom_rag_prompt 
            | self.ollama
            | self.output_parser
        )
        
        return rag_chain


