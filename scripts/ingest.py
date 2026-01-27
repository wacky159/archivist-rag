import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import settings
from src.ingestion.pipeline import run_ingestion


def check_ollama_connection() -> bool:
    try:
        import httpx

        response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def main():
    print("Archivist-RAG Ingestion")
    print("=" * 40)

    print(f"Notes path: {settings.notes_path}")
    print(f"ChromaDB path: {settings.chroma_path}")
    print(f"Embedding model: {settings.embedding_model}")
    print()

    print("Checking Ollama connection...")
    if not check_ollama_connection():
        print("Error: Cannot connect to Ollama service.")
        print(f"  Make sure Ollama is running: ollama serve")
        print(f"  Expected URL: {settings.ollama_base_url}")
        sys.exit(1)
    print("Ollama connection OK")
    print()

    print("Starting ingestion...")

    try:
        result = run_ingestion()

        print(f"\nIngestion complete!")
        print(f"  Documents processed: {result['documents']}")
        print(f"  New chunks added: {result['chunks']}")
        print(f"  Total chunks: {result.get('total_chunks', 'N/A')}")
        print(f"  Status: {result['status']}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during ingestion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
