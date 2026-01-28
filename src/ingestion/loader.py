from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader


def load_markdown_files(notes_path: Path) -> list:
    """從目錄載入 Markdown 筆記成 LangChain Documents。

    這裡刻意保持載入邏輯最精簡；切片與 metadata 增補會在 splitter 階段完成。
    """
    if not notes_path.exists():
        raise FileNotFoundError(f"Notes directory not found: {notes_path}")

    # DirectoryLoader 負責遞迴掃描與進度顯示。
    # TextLoader 確保 Markdown 一律以 UTF-8 解碼。
    loader = DirectoryLoader(
        str(notes_path),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    return loader.load()
