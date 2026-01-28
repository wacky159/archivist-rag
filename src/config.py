from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全專案的集中設定（Single Source of Truth）。

    設定值可透過 `.env`（pydantic-settings）覆寫，讓執行環境設定不必寫死在程式碼中。
    """

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
