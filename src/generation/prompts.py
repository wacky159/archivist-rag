from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

RAG_SYSTEM_TEMPLATE = """你是一個專門回答個人知識庫問題的助手。請根據以下檢索到的筆記內容回答問題。

規則：
1. 只使用提供的資料來回答，不要編造資訊
2. 在答案中使用 [1], [2] 等標記引用來源
3. 如果資料不足以回答問題，請明確說明
4. 回答完成後，列出來源清單

檢索到的筆記內容：
{context}"""

RAG_HUMAN_TEMPLATE = """{question}"""


def get_rag_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", RAG_SYSTEM_TEMPLATE),
            ("human", RAG_HUMAN_TEMPLATE),
        ]
    )


def format_docs_as_context(docs: list[dict]) -> str:
    formatted_parts = []
    for doc in docs:
        source = doc.get("source", "Unknown")
        headers = doc.get("headers", {})
        header_str = " > ".join(headers.values()) if headers else ""

        formatted_parts.append(
            f"[{doc['index']}] 來源: {source}"
            + (f" ({header_str})" if header_str else "")
            + f"\n{doc['content']}"
        )

    return "\n\n---\n\n".join(formatted_parts)
