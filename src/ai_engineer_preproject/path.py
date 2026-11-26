# ai_engineer_preproject\path.py

import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
PROJECT_ROOT = Path(os.environ["PROJECT_ROOT"]).resolve()
DATA_ROOT = PROJECT_ROOT.parent / "ai_engineer_preproject_DATA"
DOCS_DIR = DATA_ROOT / "ollama_docs"
LOCAL_EMBED_MODEL = DATA_ROOT / "local_embed_model"
CHUNK_EMBEDINGS = DATA_ROOT / "chunk_embeddings" / "chunk_embeddings.npy"
INDEXES = DATA_ROOT / "local_indexes" / "MY_index.faiss"
OLLAMA_URL = "http://localhost:11434"
LLM_MODEL = "qwen2.5:1.5b"
