from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader


def load_markdown_files(notes_path: Path) -> list:
    if not notes_path.exists():
        raise FileNotFoundError(f"Notes directory not found: {notes_path}")

    loader = DirectoryLoader(
        str(notes_path),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    return loader.load()
