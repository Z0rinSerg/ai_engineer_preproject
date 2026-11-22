import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(
        self, 
        embed_model_name: str, 
        index: faiss.Index, 
        chunks: list[dict]
    ):
        """
        Инициализация векторного хранилища.
        
        :param embed_model_name: Название модели для эмбеддингов.
        :param index: Построенный индекс FAISS.
        :param chunks: Список словарей с данными {'text': ..., 'source': ...}.
        """
        self.embed_model = SentenceTransformer(embed_model_name)
        self.index = index
        self.chunks = chunks

    def search(self, question: str, top_k: int = 3) -> list[dict]:
        """Возвращает top_k чанков, наиболее близких к запросу по смыслу."""
        # 1. Считаем эмбеддинг запроса
        query_emb = self.embed_model.encode(
            [question],
            normalize_embeddings=True,
        ).astype(np.float32)

        # 2. Ищем ближайших соседей
        scores, indices = self.index.search(query_emb, top_k)

        # 3. Собираем результат с метаданными
        results = []
        for score, idx in zip(scores[0], indices[0]):
            # Защита от выхода за границы, если индекс пуст или поврежден
            if idx == -1 or idx >= len(self.chunks):
                continue
            
            results.append({
                "text": self.chunks[idx]["text"],
                "source": self.chunks[idx]["source"],
                "score": float(score),
            })
        return results