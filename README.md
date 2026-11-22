# ai_engineer_preproject

Рабочая папка для пред-проекта AI-инженера. 
Для бесплатной части курса Яндекс Практикум - `"ИИ - Инженер"`

## Стек
- `Python 3.12`
- `uv`
- `git`
- `VSCode`
- `Jupyter Notebooks` (.ipynb) в VSCode
- MCP-серверы (FastMCP / mcp)
- `ollama` сервер для локальных моделей LLM
- `docker` 



## Быстрый старт 

1. Установка `uv` (если он еще не установлен).
Для Linux:

```bash 
curl -LsSf https://astral.sh/uv/install.sh | sh
```
для [Windows](docs/DEPLOYMENT.md#установка-uv)

2. Установка `git` (если он еще не установлен).
Для Linux:
```bash
sudo apt update
sudo apt install git
```
проверка установки:
```bash
git --version
```



### Клонирование папки репозитория
```bash
git clone https://github.com/Z0rinSerg/ai_engineer_preproject

cd ai_engineer_preproject
```
### Установка (синхронизация) зависимостей, создание окружения
```bash
uv sync
```
### Активация виртуального окружения
```bash
source .venv/bin/linux  # для Linux/macOS
```
```bash
 .\.venv\Scripts\activate.ps1  # для Windows
```
### Запуск VS Code (в корне проекта)
```bash
code .
```

## Быстрый тест 
### Запуск шаблона (заглушки) MCP сервера в отдельном окне терминала
```bash
uv run python .\scripts\mcp_server.py    
```
### запуск файла с обращением к MCP серверу (в другом окне терминала)
```bash
uv run python test_local.py
```
в выводе должно быть data='Hello, Сергей! MCP server is running.'

## Структура проекта
- `docs/` - документация проекта 
- `notebooks/` — ноутбуки для исследований
- `src/ai_engineer_preproject/` — основной код (библиотека)
- `scripts/` — утилиты и запуск MCP-серверов
- `ollama_docs` - в контексте проекта - это не документация - это датасет для работы с LLM (ollama)

## Функциональная структура
- Функции проекта выносятся в `src/ai_engineer_preproject/__init__.py` и импортируются непосредственно 
  в начало ноутбука или в ячейку перед использованием
- в проекте [ведется файл **.env**](docs/ENV.md) с переменными среды зависящими от платформы (Linux \ Windows) 
  на каждой платформе он свой, прописан в .gitignore (не коммитится) в основном содержит пути или URL. 

## Подробно о сборке стека
Процесс сборки среды проекта и стека инструментов описан в файле документации  [DEPLOYMENTS.md](docs/DEPLOYMENT.md)
Стек в данном проекте более современный чем, то что предлагается использовать на курсе. Описание (не полное) действий с инструментами в процессе прохождения курса в [данном файле.](docs/LESSONS_NOTES.md)
## Основные направления при сборке стека

Основные направления, которых придерживаюсь при сборке стека описаны в файле [CLAUDE.md](docs/CLAUDE.md)
не всегда реализуются на 100%
Файл заимствован из репозитория:
https://github.com/justxor/pythonroamap2026/ 
