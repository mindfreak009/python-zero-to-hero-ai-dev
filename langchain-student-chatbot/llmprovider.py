from langchain_ollama import ChatOllama
from config import OLLAMA_CHAT_MODEL


# ================================================
# CREATE OLLAMA LLM 
# ================================================

def get_llm():
    llm = ChatOllama(
        model = OLLAMA_CHAT_MODEL,
        temperature = 0 
    )

    return llm