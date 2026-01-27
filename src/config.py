from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    notes_path: Path = Path("./sample_notes")
    chroma_path: Path = Path("./data/chroma")
    chroma_collection_name: str = "archivist_notes"

    ollama_base_url: str = "http://localhost:11434"
    embedding_model: str = "nomic-embed-text"
    llm_model: str = "llama3.2"

    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_top_k: int = 5

    enable_compression: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
