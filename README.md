# ai_engineer_preproject

Рабочая папка для пред-проекта AI-инженера.

## Стек
- Python 3.12
- uv
- Jupyter Notebooks (.ipynb) в VSCode
- MCP-серверы (FastMCP / mcp)

## Быстрый старт
```bash
# Установка зависимостей
uv sync

# Активация виртуального окружения
source .venv/bin/linux  # для Linux/macOS
# .venv\Scripts\activate  # для Windows

# Запуск Jupyter Lab
uv run jupyter lab
```

## Структура
- `notebooks/` — ноутбуки для исследований
- `src/ai_engineer_preproject/` — основной код (библиотека)
- `scripts/` — утилиты и запуск MCP-серверов