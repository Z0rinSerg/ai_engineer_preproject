def main() -> None:
    print("Hello from ai-engineer-preproject!")


#В __init__.py можно задать список имён, которые будут автоматически 
# экспортироваться при импорте самого пакета

__all__ = ['VectorStore' , 'chank_text' ,'set_environment_variables']
# Теперь при импорте всего пакета:
# from ai_engineer_preproject import * 
# автоматически импортируются только указанные имена 
# VectorStore , chunk_text ...