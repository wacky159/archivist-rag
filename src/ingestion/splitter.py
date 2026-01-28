import hashlib
from typing import Any

import frontmatter
from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from src.config import settings

# Header-aware 切片會把筆記結構保留在 metadata 中，
# 同時提升檢索品質（能在章節語意內匹配）與 UI 呈現（可顯示麵包屑）。
HEADERS_TO_SPLIT_ON = [
    ("#", "header_1"),
    ("##", "header_2"),
    ("###", "header_3"),
]


def extract_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """解析 YAML frontmatter，回傳 (metadata, 去除 frontmatter 的內容)。

    ChromaDB 的 metadata 值必須是 primitive 型別。Frontmatter 常見會有 list（tags）
    與 date 等型別，因此在這裡先做正規化以避免寫入向量庫時失敗。
    """
    try:
        parsed = frontmatter.loads(content)
        metadata = dict(parsed.metadata)
        # 轉換複雜型別為 ChromaDB 可接受的值（str, int, float, bool）
        for key, value in metadata.items():
            if isinstance(value, list):
                metadata[key] = ", ".join(str(v) for v in value)
            elif not isinstance(value, (str, int, float, bool, type(None))):
                metadata[key] = str(value)
        return metadata, parsed.content
    except Exception:
        return {}, content


def compute_file_hash(content: str) -> str:
    """用於增量 ingestion 的穩定內容雜湊值。"""
    return hashlib.md5(content.encode()).hexdigest()


def split_markdown_document(doc: Document) -> list[Document]:
    """將單篇 Markdown 文件切成 chunks。

    策略：
    1) 先依 Markdown 標題切片以保留語意結構。
    2) 若某個章節仍過大，再使用遞迴切片作為保底。
    3) 為每個 chunk 補上 source + file_hash + frontmatter metadata。
    """
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

    # 保底：確保 chunk 大小落在模型/向量庫較友善的範圍。
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
        # metadata 用來支援引用（source）、麵包屑（headers）以及可重跑 ingestion（file_hash）。
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
