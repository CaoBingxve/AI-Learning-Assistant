from pathlib import Path

from langchain_chroma import Chroma

from ai.rag.embeddings import embeddings


BACKEND_ROOT = Path(__file__).resolve().parents[2]

CHROMA_DIR = BACKEND_ROOT / "data" / "chroma"


vector_store = Chroma(
    collection_name="learning_knowledge",

    embedding_function=embeddings,

    persist_directory=str(CHROMA_DIR)
)


retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 3
    }
)