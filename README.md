# ai_engineer_preproject

Рабочая папка для пред-проекта AI-инженера. 
Для бесплатной части курса Яндекс Практикум - "ИИ - Инженер"

## Стек
- Python 3.12
- uv
- Jupyter Notebooks (.ipynb) в VSCode
- MCP-серверы (FastMCP / mcp)

## Быстрый старт

### Клонирование папки репозитория
```bash
 git clone https://github.com/Z0rinSerg/ai_engineer_preproject
```
### Установка зависимостей
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

## Подробно о сборке стека
Процесс сборки среды описан в файле документации  [DEPLOYMENTS.md](docs/DEPLOYMENT.md)

## Основные направления при сборке стека

Основные направления, которых придерживаюсь при сборке стека описаны в файле [CLAUDE.md](docs/CLAUDE.md)
не всегда реализуются на 100%
Файл заимствован из репозитория:
https://github.com/justxor/pythonroamap2026/  