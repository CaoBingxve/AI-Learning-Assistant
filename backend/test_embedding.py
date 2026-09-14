from ai.rag.embeddings import embeddings


texts = [
    "学习记录中的 study_time 单位统一使用分钟。"
]


print("开始生成向量...")


vectors = embeddings.embed_documents(
    texts
)


print("向量生成成功")

print("文档数量：", len(vectors))

print("向量维度：", len(vectors[0]))

print("前5个数字：", vectors[0][:5])