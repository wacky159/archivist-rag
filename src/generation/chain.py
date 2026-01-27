from collections.abc import Iterator
from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

from src.config import settings
from src.generation.prompts import format_docs_as_context, get_rag_prompt
from src.retrieval.chain import retrieve_with_sources


def get_llm() -> ChatOllama:
    return ChatOllama(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=0.7,
    )


def create_rag_chain():
    prompt = get_rag_prompt()
    llm = get_llm()
    output_parser = StrOutputParser()

    return prompt | llm | output_parser


def invoke_rag(question: str) -> dict[str, Any]:
    sources = retrieve_with_sources(question)

    if not sources:
        return {
            "answer": "抱歉，在筆記中找不到相關資訊來回答這個問題。",
            "sources": [],
        }

    context = format_docs_as_context(sources)
    chain = create_rag_chain()

    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return {
        "answer": answer,
        "sources": sources,
    }


def stream_rag(question: str) -> Iterator[dict[str, Any]]:
    sources = retrieve_with_sources(question)

    if not sources:
        yield {
            "type": "answer",
            "content": "抱歉，在筆記中找不到相關資訊來回答這個問題。",
        }
        yield {"type": "sources", "content": []}
        return

    yield {"type": "sources", "content": sources}

    context = format_docs_as_context(sources)
    chain = create_rag_chain()

    for chunk in chain.stream(
        {
            "context": context,
            "question": question,
        }
    ):
        yield {"type": "token", "content": chunk}

    yield {"type": "done", "content": None}
