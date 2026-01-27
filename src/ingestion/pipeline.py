from pathlib import Path

from langchain_chroma import Chroma

from src.config import settings
from src.embeddings import get_embeddings
from src.ingestion.loader import load_markdown_files
from src.ingestion.splitter import split_documents


def get_existing_hashes(vectorstore: Chroma) -> set[str]:
    try:
        results = vectorstore.get(include=["metadatas"])
        if results and results.get("metadatas"):
            return {
                m.get("file_hash") for m in results["metadatas"] if m.get("file_hash")
            }
    except Exception:
        pass
    return set()


def delete_documents_by_hash(vectorstore: Chroma, file_hash: str) -> None:
    try:
        results = vectorstore.get(where={"file_hash": file_hash}, include=["metadatas"])
        if results and results.get("ids"):
            vectorstore.delete(ids=results["ids"])
    except Exception:
        pass


def run_ingestion(
    notes_path: Path | None = None,
    chroma_path: Path | None = None,
) -> dict:
    notes_path = notes_path or settings.notes_path
    chroma_path = chroma_path or settings.chroma_path

    chroma_path.mkdir(parents=True, exist_ok=True)

    documents = load_markdown_files(notes_path)
    if not documents:
        return {"documents": 0, "chunks": 0, "status": "no documents found"}

    chunks = split_documents(documents)

    embeddings = get_embeddings()
    vectorstore = Chroma(
        collection_name=settings.chroma_collection_name,
        embedding_function=embeddings,
        persist_directory=str(chroma_path),
    )

    existing_hashes = get_existing_hashes(vectorstore)
    new_chunks = []
    updated_hashes = set()

    for chunk in chunks:
        file_hash = chunk.metadata.get("file_hash")
        if file_hash and file_hash not in existing_hashes:
            if file_hash not in updated_hashes:
                delete_documents_by_hash(vectorstore, file_hash)
                updated_hashes.add(file_hash)
            new_chunks.append(chunk)

    if new_chunks:
        vectorstore.add_documents(new_chunks)

    return {
        "documents": len(documents),
        "chunks": len(new_chunks),
        "total_chunks": len(chunks),
        "status": "success",
    }
