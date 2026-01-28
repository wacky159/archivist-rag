from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_ollama import ChatOllama

from src.config import settings
from src.retrieval.multi_query import get_multi_query_retriever
from src.retrieval.vectorstore import get_retriever


def get_compression_retriever():
    """Multi-Query 檢索 +（可選）LLM contextual compression。

    Compression 用延遲（多一次 LLM 呼叫）換取更乾淨的 context：
    只抽取每個檢索 chunk 中與問題相關的片段。
    """
    base_retriever = get_multi_query_retriever()

    # temperature=0 讓抽取結果更穩定、偏向事實。
    llm = ChatOllama(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )

    compressor = LLMChainExtractor.from_llm(llm)

    return ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever,
    )


def get_retrieval_chain():
    """依照設定選擇檢索策略。"""
    if settings.enable_compression:
        return get_compression_retriever()
    return get_multi_query_retriever()


def retrieve_with_sources(query: str) -> list[dict]:
    """檢索相關 chunks，並整理成方便 UI/prompt 使用的資料結構。"""
    retriever = get_retrieval_chain()
    docs = retriever.invoke(query)

    results = []
    for i, doc in enumerate(docs):
        results.append(
            {
                "index": i + 1,
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "headers": {
                    k: v for k, v in doc.metadata.items() if k.startswith("header_")
                },
                "metadata": doc.metadata,
            }
        )

    return results
