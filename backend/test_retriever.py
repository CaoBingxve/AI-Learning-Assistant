from ai.rag.vector_store import retriever


print("开始检索...")


docs = retriever.invoke(
    "Copilot的内部测试代号是什么？"
)


print("检索成功")

print("检索到：", len(docs), "个文档")


for index, doc in enumerate(
    docs,
    start=1
):
    print(f"\n--- 文档 {index} ---")

    print(doc.page_content)

    print(doc.metadata)