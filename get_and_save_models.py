print("Импорт библиотеки для работы с эмбедингами...")
import os
import getpass # Модуль для скрытого ввода (правильный импорт) 
from urllib.parse import quote # Функция для экранирования URL (правильный импорт)
from huggingface_hub import snapshot_download
from sentence_transformers import SentenceTransformer
print("Импорт ОК.")

password = getpass.getpass(prompt='Введите пароль для прокси-сервера: ')
domain = "d0"
username = "zorin_sv"
full_username = f"{domain}\\{username}"
encoded_username = quote(full_username, safe='')
encoded_password = quote(password, safe='')

proxy_url = f"http://{encoded_username}:{encoded_password}@proxy-http-006.d0.vsw.ru:3128"

# Настройка прокси только для процесса
os.environ['HTTP_PROXY'] = proxy_url
os.environ['HTTPS_PROXY'] = proxy_url

# http://proxy-http-006.d0.vsw.ru:3128
# Принудительная загрузка модели в кэш через прокси

print(f"Загружаем модель эмбеддингов...")
model_path = snapshot_download(
    repo_id="sentence-transformers/all-MiniLM-L6-v2",
    proxies={"http": proxy_url, "https": proxy_url}
)
embed_model = SentenceTransformer(model_path)
print(f"Модель ембеддингов {embed_model._get_name()} загружена")

# # Загрузка модели с сайта HF
# EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# print(f"Загружаем модель эмбеддингов: {EMBED_MODEL}")
# embed_model = SentenceTransformer(EMBED_MODEL)
# print(f"Модель ембеддингов загружена - сохраняем...")

# # ===!!!=== ТОЛЬКО ДЛЯ ЛОКАЛЬНОГО СОХРАНЕНИЯ МОДЕЛИ ЕМБЕДДИНГОВ ===!!!=== 
# # Файловый размер модели около 450 мегабайт
embed_model.save('local_embed_model')
print(f"Модель ембеддингов сохранена")

