from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from ai.llm import llm
from ai.prompts import rag_prompt
from ai.rag.vector_store import retriever

# Document[]→str
def format_documents(documents):

    return "\n\n".join(
        document.page_content
        for document in documents
    )

rag_chain=(
    {
        "context":retriever|format_documents,
        "question":RunnablePassthrough()
    }
    | rag_prompt
    | llm
    | StrOutputParser()
)