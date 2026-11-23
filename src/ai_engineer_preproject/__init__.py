# Импортируем в пакет проекта -> 
# функции и классы из файла prj_functions.py и prj_classes.py соответственно
from .prj_functions import chunk_text
from .prj_classes import VectorStore, VecIdxSearch

def main() -> None:
    print("Hello from ai-engineer-preproject!")

#В __init__.py можно задать список имён, которые будут автоматически 
# экспортироваться при импорте самого пакета, т.е. т.н. 

# Определение публичного API пакета проекта

__all__ = [
    'VecIdxSearch',
    'VectorStore',
    'chunk_text'
    ]
# Теперь при импорте всего пакета:
# from ai_engineer_preproject import * 
# автоматически импортируются только указанные имена 
# VectorStore , chunk_text ...