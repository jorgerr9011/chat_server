from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.query_constructor.base import get_query_constructor_prompt
from .rag import get_retriever, format_docs

class QaLlm: 
    
    def __init__(self):
        
        self.ollama = Ollama(base_url='http://localhost:11434', model="phi3")
        self.output_parser = StrOutputParser()
        
        self.contextualize_q_system_prompt = """Given a chat history and the latest user question which might reference context in the chat history, formulate /
        a standalone question which can be understood without the chat history. Do not answer the question, just reformulate it if needed and /
        otherwise return it as is."""

        self.contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.contextualize_q_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
        self.contextualize_q_chain = (self.contextualize_q_prompt | self.ollama | StrOutputParser())

        self.template = """You are a technical support specialist in an IT department who are specialized in resolve incidences, answer queries and provide assistance. /
        Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't /
        try to make up an answer. If you don't find any relevant information to the question, don't talk about it and just say "Sorry I can't help you with that".

        {context}"""
            
        self.custom_rag_prompt = PromptTemplate.from_template(self.template)
        
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

    def contextualized_question(self, input: dict):
        if input.get("chat_history"):
            return self.contextualize_q_chain
        else:
            return input["question"]
        
    def getMessages(self):
        messages = []
        return messages

    def chain(self):
        
        retriever = get_retriever()
        
        rag_chain = (
            RunnablePassthrough.assign(context=self.contextualize_q_chain | retriever | format_docs)
            | self.qa_prompt
            | self.ollama
        )
        return rag_chain
        