from pathlib import Path
from dotenv import load_dotenv

# Функция для загрузки переменных окружения из файла .env
def set_environment_variables():
    # Загружаем переменные окружения из файла .env
    load_dotenv()

    # Устанавливаем переменные среды
    os.environ["PROJECT_ROOT"] = Path(os.getenv("PROJECT_ROOT")).as_posix()
    os.environ["OLLAMA_DOCS"] = Path(os.getenv("OLLAMA_DOCS")).as_posix()
    os.environ["OLLAMA_URL"] = os.getenv("OLLAMA_URL")