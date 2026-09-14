from ai.rag.vector_store import retriever


docs = retriever.invoke(
    "学习记录中的学习时间是什么单位？"
)


for index, doc in enumerate(
    docs,
    start=1
):

    print(
        f"\n--- 检索结果 {index} ---"
    )

    print(
        doc.page_content
    )

    print(
        doc.metadata
    )