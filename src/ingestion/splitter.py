import hashlib
from typing import Any

import frontmatter
from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from src.config import settings

HEADERS_TO_SPLIT_ON = [
    ("#", "header_1"),
    ("##", "header_2"),
    ("###", "header_3"),
]


def extract_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    try:
        parsed = frontmatter.loads(content)
        metadata = dict(parsed.metadata)
        # Convert complex types to ChromaDB-compatible values (str, int, float, bool)
        for key, value in metadata.items():
            if isinstance(value, list):
                metadata[key] = ", ".join(str(v) for v in value)
            elif not isinstance(value, (str, int, float, bool, type(None))):
                metadata[key] = str(value)
        return metadata, parsed.content
    except Exception:
        return {}, content


def compute_file_hash(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()


def split_markdown_document(doc: Document) -> list[Document]:
    original_content = doc.page_content
    source_path = doc.metadata.get("source", "unknown")

    frontmatter_metadata, content_without_frontmatter = extract_frontmatter(
        original_content
    )
    file_hash = compute_file_hash(original_content)

    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False,
    )
    header_splits = header_splitter.split_text(content_without_frontmatter)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    final_chunks = []
    for split in header_splits:
        if len(split.page_content) > settings.chunk_size:
            sub_chunks = text_splitter.split_documents([split])
            final_chunks.extend(sub_chunks)
        else:
            final_chunks.append(split)

    for chunk in final_chunks:
        chunk.metadata.update(
            {
                "source": source_path,
                "file_hash": file_hash,
                **frontmatter_metadata,
            }
        )

    return final_chunks


def split_documents(documents: list[Document]) -> list[Document]:
    all_chunks = []
    for doc in documents:
        chunks = split_markdown_document(doc)
        all_chunks.extend(chunks)
    return all_chunks
