import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st

from src.generation.chain import stream_rag
from src.retrieval.vectorstore import get_vectorstore


def check_ollama_connection() -> bool:
    try:
        import httpx
        from src.config import settings

        response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def check_database_has_documents() -> bool:
    try:
        vectorstore = get_vectorstore()
        results = vectorstore.get(limit=1)
        return bool(results and results.get("ids"))
    except Exception:
        return False


def display_sources(sources: list[dict]):
    if not sources:
        return

    with st.expander(f"📚 參考來源 ({len(sources)} 個)", expanded=False):
        for source in sources:
            source_path = Path(source["source"]).name
            headers = source.get("headers", {})
            header_str = " > ".join(headers.values()) if headers else ""

            st.markdown(
                f"**[{source['index']}] {source_path}**"
                + (f" - {header_str}" if header_str else "")
            )
            st.markdown(
                f"```\n{source['content'][:500]}{'...' if len(source['content']) > 500 else ''}\n```"
            )
            st.divider()


def main():
    st.set_page_config(
        page_title="Archivist-RAG",
        page_icon="📚",
        layout="wide",
    )

    st.title("📚 Archivist-RAG")
    st.caption("個人 Markdown 知識庫問答系統")

    if not check_ollama_connection():
        st.error("⚠️ 無法連接到 Ollama 服務。請確保 Ollama 正在運行：`ollama serve`")
        st.stop()

    if not check_database_has_documents():
        st.warning("⚠️ 向量資料庫是空的。請先執行 ingestion：`python scripts/ingest.py`")
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "sources" not in st.session_state:
        st.session_state.sources = {}

    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and i in st.session_state.sources:
                display_sources(st.session_state.sources[i])

    if prompt := st.chat_input("輸入你的問題..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            sources_placeholder = st.empty()

            full_response = ""
            current_sources = []

            with st.spinner("思考中..."):
                for event in stream_rag(prompt):
                    if event["type"] == "sources":
                        current_sources = event["content"]
                    elif event["type"] == "token":
                        full_response += event["content"]
                        message_placeholder.markdown(full_response + "▌")
                    elif event["type"] == "done":
                        message_placeholder.markdown(full_response)

            if current_sources:
                with sources_placeholder.container():
                    display_sources(current_sources)

        message_index = len(st.session_state.messages)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
        st.session_state.sources[message_index] = current_sources


if __name__ == "__main__":
    main()
