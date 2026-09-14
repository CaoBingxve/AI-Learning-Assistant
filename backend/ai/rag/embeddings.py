from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer


class LocalOnnxEmbeddings(Embeddings):

    def __init__(self):

        self.model = SentenceTransformer(
            "BAAI/bge-small-zh-v1.5",
            backend="onnx",
            model_kwargs={
                "provider": "CPUExecutionProvider"
            }
        )


    def embed_documents(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return vectors.tolist()


    def embed_query(
        self,
        text: str
    ) -> list[float]:

        vector = self.model.encode(
            [text],
            normalize_embeddings=True
        )[0]

        return vector.tolist()


embeddings = LocalOnnxEmbeddings()