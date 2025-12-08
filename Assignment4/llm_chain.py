import os
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from typing import List, Dict

class LLMChainHandler:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.llm = self._initialize_llm()
        self.prompt = self._initialize_prompt()
        self.chain = self.prompt | self.llm 

    def _initialize_llm(self):
        if self.provider == "ollama":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", "llama3")
            print(f"Initializing Ollama LLM (model: {model}, url: {base_url})")
            return ChatOllama(base_url=base_url, model=model)
        
        elif self.provider == "openai":
            # This covers LM Studio, OpenRouter, etc.
            api_key = os.getenv("OPENAI_API_KEY", "sk-dummy")
            base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1")
            model = os.getenv("OPENAI_MODEL", "local-model")
            print(f"Initializing OpenAI-compatible LLM (model: {model}, url: {base_url})")
            return ChatOpenAI(api_key=api_key, base_url=base_url, model_name=model)
        
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _initialize_prompt(self):
        template = """
        You are a helpful assistant. You have access to the following information from the database:

        CONTEXT:
        {context}

        QUESTION:
        {question}

        ANSWER (based on the context provided):
        """
        return PromptTemplate(template=template, input_variables=["context", "question"])

    def query(self, question: str, context_docs: List[Dict]) -> str:
        # Format context
        context_text = "\n\n".join([f"- {doc.get('content', '')}" for doc in context_docs])
        
        # Invoke chain
        response = self.chain.invoke({"context": context_text, "question": question})
        
        # Handle different response types (str vs message)
        if hasattr(response, 'content'):
            return response.content
        return str(response)
