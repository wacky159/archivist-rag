from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_ollama import ChatOllama

from src.config import settings
from src.retrieval.vectorstore import get_retriever


def get_multi_query_retriever():
    """透過把使用者問題改寫成多個版本來提升召回率（recall）。

    個人筆記常有用詞不一致；Multi-Query 會用 LLM 產生替代查詢，
    提高檢索到正確 chunks 的機率。
    """
    base_retriever = get_retriever()

    # 這裡偏好 deterministic：我們要的是穩定的查詢變體。
    llm = ChatOllama(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )

    return MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm,
    )
