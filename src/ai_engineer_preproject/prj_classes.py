from typing import Set
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

#--------------------------------------------------------------------
# VectorStore
#--------------------------------------------------------------------
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
#---------------------------------------------------------------------------------------
# VecIdxSearch 
# ---------------------------------------------------------------------------------------

class VecIdxSearch:
    """ Векторное хранилище для поиска по смыслу в локальных текстовых файлах.

    Класс автоматически читает файлы из указанной директории, нарезает их на чанки, 
    создает эмбеддинги c помощью SentenceTransformer и строит индекс FAISS.
    Пример использования: 
        >>> store = VecIdxSearch("./my_docs")
        >>> results = store.search("как работает faiss", top_k=5)
    
    Attributes:
        data_dir (Path): Путь к директории c исходными файлами.
        embed_model (SentenceTransformer): Загруженная модель для эмбеддингов.
        index (faiss.Index): Построенный индекс для быстрого поиска.
        chunks (List[Dict]): Список словарей c текстом чанка и источником.
    """

    def __init__(
        self, 
        data_dir: str,
        embed_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        index_factory: str = "IVF256,Flat",
        chunk_max_chars: int = 800,
        chunk_min_chars: int = 50,
        extensions: Set[str] = None
    ):
        """
        Инициализация векторного хранилища из каталога с файлами.
        
        :param data_dir: Путь к папке с файлами.
        :param embed_model_name: Название модели для эмбеддингов.
        :param index_factory: Строка-конфиг для faiss.index_factory.
        :param chunk_max_chars: Максимальная длина чанка.
        :param chunk_min_chars: Минимальная длина чанка.
        :param extensions: Множество расширений (например, {'.md', '.txt', '.mdx'}). 
                           Символ '*' не поддерживается. Если передано пустое множество,
                           используются значения по умолчанию.
        """
        self.data_dir = Path(data_dir)
        self.embed_model_name = embed_model_name
        self.embed_model = SentenceTransformer(embed_model_name)
        self.index_factory = index_factory
        self.chunk_max_chars = chunk_max_chars
        self.chunk_min_chars = chunk_min_chars
        self._doc_count: int = 0 # Новый атрибут
        
        # 1. Обработка расширений: защита от пустого множества
        default_exts = {'.md', '.txt', '.mdx'}
        
        if extensions is None or len(extensions) == 0:
            self.extensions = default_exts
        else:
            # Приводим к нижнему регистру и фильтруем (на случай, если передали "MD" или пустые строки)
            self.extensions = {
                ext.lower().strip() for ext in extensions if ext.strip()
            }
            # Дополнительная страховка: если после фильтрации осталось пусто
            if not self.extensions:
                self.extensions = default_exts

        self.chunks = []
        self.index = None
        
        self._build_index()
    @property
    def num_documents(self) -> int:
        """
        Количество исходных документов (файлов), которые были успешно прочитаны 
        и использованы для построения индекса.
        
        Returns:
            int: Число файлов-источников.
        """
        return self._doc_count    
    @property 
    def num_chunks(self) -> int:
        """ Количество текстовых чанков, содержащихся в индексе.
        Returns:
            int: Число чанков.
        """
        return len(self.chunks)


    def _collect_files(self) -> list[Path]:
        """Собирает список файлов строго по заданному списку расширений."""
        if not self.data_dir.exists() or not self.data_dir.is_dir():
            raise ValueError(f"Директория {self.data_dir} не существует")

        files = []
        for ext in self.extensions:
            # Ищем файлы с конкретным расширением (регистрочувствительно к имени файла, 
            # но расширение мы привели к нижнему регистру выше)
            pattern = f"*{ext}"
            files.extend(self.data_dir.rglob(pattern))
        
        return [p for p in files if p.is_file()]

    def _read_file(self, file_path: Path) -> str:
        """Читает текстовый файл. 
        Исключена обработка cp1251 и пропуск бинарных файлов: 
        если файл не в utf-8, возникнет исключение.
        """
        return file_path.read_text(encoding="utf-8")

    @staticmethod
    def chunk_text(text: str, max_chars: int = 800, min_chars: int = 50) -> list[str]:
        """Режет Markdown по заголовкам ##; длинные секции дробит по параграфам."""
        lines = text.split("\n")
        sections, current = [], []
        for line in lines:
            if line.startswith("## ") and current:
                sections.append("\n".join(current).strip())
                current = [line]
            else:
                current.append(line)
        if current:
            sections.append("\n".join(current).strip())

        chunks = []
        for section in sections:
            if not section:
                continue
            if len(section) <= max_chars:
                chunks.append(section)
                continue
            buf = ""
            for paragraph in section.split("\n\n"):
                if len(buf) + len(paragraph) + 2 <= max_chars:
                    buf = f"{buf}\n\n{paragraph}" if buf else paragraph
                else:
                    if buf:
                        chunks.append(buf.strip())
                    buf = paragraph
            if buf:
                chunks.append(buf.strip())

        return [c for c in chunks if len(c) >= min_chars]

    def _build_index(self):
        """Считывает файлы, нарезает на чанки, создает эмбеддинги и строит индекс FAISS."""
        
        files = self._collect_files()
        if not files:
            raise ValueError(
                f"В директории {self.data_dir} не найдено файлов с расширениями: {self.extensions}"
            )
        # Устанавливаем количество загруженных документов
        self._doc_count = len(files)

        temp_chunks = []
        for file_path in files:
            # Теперь здесь будет падать ошибка, если файл не текстовый или не в utf-8
            text = self._read_file(file_path)
            if not text.strip():
                continue
                
            chunks = self.chunk_text(
                text, 
                self.chunk_max_chars, 
                self.chunk_min_chars
            )
            for chunk in chunks:
                temp_chunks.append({
                    "text": chunk,
                    "source": str(file_path.name)
                })

        if not temp_chunks:
            raise ValueError("После чанкинга не осталось ни одного валидного фрагмента текста.")
            
        self.chunks = temp_chunks

        texts = [c["text"] for c in self.chunks]
        embeddings = self.embed_model.encode(
            texts, 
            normalize_embeddings=True,
            show_progress_bar=True
        ).astype(np.float32)

        d = embeddings.shape[1]
        self.index = faiss.index_factory(d, self.index_factory)
        
        if not self.index.is_trained:
            self.index.train(embeddings)
            
        self.index.add(embeddings)

    def search(self, question: str, top_k: int = 3) -> list[dict]:
        """Возвращает top_k чанков, наиболее близких к запросу по смыслу."""
        if self.index is None or not self.chunks:
            return []

        query_emb = self.embed_model.encode(
            [question],
            normalize_embeddings=True,
        ).astype(np.float32)

        scores, indices = self.index.search(query_emb, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or idx >= len(self.chunks):
                continue
            
            results.append({
                "text": self.chunks[idx]["text"],
                "source": self.chunks[idx]["source"],
                "score": float(score),
            })
        return results