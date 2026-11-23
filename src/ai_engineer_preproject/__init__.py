def main() -> None:
    print("Hello from ai-engineer-preproject!")

from .prj_functions import chunk_text
from .prj_classes import VectorStore
#В __init__.py можно задать список имён, которые будут автоматически 
# экспортироваться при импорте самого пакета, т.е. т.н. 
# Определение публичного API пакета проекта

__all__ = [
    'VectorStore',
    'chunk_text'
    ]
# Теперь при импорте всего пакета:
# from ai_engineer_preproject import * 
# автоматически импортируются только указанные имена 
# VectorStore , chunk_text ...