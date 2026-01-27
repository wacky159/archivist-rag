from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_ollama import ChatOllama

from src.config import settings
from src.retrieval.vectorstore import get_retriever


def get_multi_query_retriever():
    base_retriever = get_retriever()

    llm = ChatOllama(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )

    return MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm,
    )
