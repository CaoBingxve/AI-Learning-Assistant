from sentence_transformers import SentenceTransformer


print("开始加载 ONNX 模型...")


model = SentenceTransformer(
    "BAAI/bge-small-zh-v1.5",
    backend="onnx",
    model_kwargs={
        "provider": "CPUExecutionProvider"
    }
)


print("模型加载成功")

print("开始 encode...")


vectors = model.encode(
    [
        "学习记录中的 study_time 单位统一使用分钟。"
    ],
    normalize_embeddings=True
)


print("encode成功")

print("shape:", vectors.shape)

print("前5维:", vectors[0][:5])