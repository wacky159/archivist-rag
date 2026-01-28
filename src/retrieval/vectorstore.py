from langchain_chroma import Chroma

from src.config import settings
from src.embeddings import get_embeddings


def get_vectorstore() -> Chroma:
    """連線到本專案使用的 Chroma collection（落地持久化）。"""
    embeddings = get_embeddings()
    return Chroma(
        collection_name=settings.chroma_collection_name,
        embedding_function=embeddings,
        persist_directory=str(settings.chroma_path),
    )


def get_retriever(top_k: int | None = None):
    """回傳 similarity search（top-k）的 retriever 包裝器。"""
    vectorstore = get_vectorstore()
    return vectorstore.as_retriever(
        search_kwargs={"k": top_k or settings.retrieval_top_k}
    )
