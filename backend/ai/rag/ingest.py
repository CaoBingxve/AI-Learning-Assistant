from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ai.rag.vector_store import vector_store


BACKEND_ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_DIR = BACKEND_ROOT / "knowledge"


def load_documents():
    documents = []

    for file_path in KNOWLEDGE_DIR.iterdir():

        if file_path.suffix not in {".txt", ".md"}:
            continue

        content = file_path.read_text(
            encoding="utf-8"
        )

        document = Document(
            page_content=content,
            metadata={
                "source": file_path.name
            }
        )

        documents.append(document)

    return documents


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=[
            "\n\n",
            "\n",
            "。",
            "！",
            "？",
            "；",
            "，",
            " ",
            ""
        ]
    )

    return text_splitter.split_documents(
        documents
    )


def build_knowledge_base():
    print("开始构建知识库...")

    documents = load_documents()

    print(
        f"读取到 {len(documents)} 个文档"
    )

    chunks = split_documents(
        documents
    )

    print(
        f"切分得到 {len(chunks)} 个片段"
    )

    vector_store.add_documents(
        chunks
    )

    print(
        f"知识库构建完成，共写入 {len(chunks)} 个片段"
    )


if __name__ == "__main__":
    build_knowledge_base()