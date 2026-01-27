from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_ollama import ChatOllama

from src.config import settings
from src.retrieval.multi_query import get_multi_query_retriever
from src.retrieval.vectorstore import get_retriever


def get_compression_retriever():
    base_retriever = get_multi_query_retriever()

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
    if settings.enable_compression:
        return get_compression_retriever()
    return get_multi_query_retriever()


def retrieve_with_sources(query: str) -> list[dict]:
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
