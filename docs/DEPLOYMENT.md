# Описание (заметки) процесса создания среды разработки и анализа в проекте

## Создание папки проекта и переход в нее 

```bash
mkdir ai_engineer_preproject && cd ai_engineer_preproject
```
## Синхронизация с GitHub

### Первичная синхронизация в локальной новой среде 

```bash
git clone https://github.com/Z0rinSerg/ai_engineer_preproject
```

### При создании нового проекта "с нуля"
Создается соответсвующая структура (папка `.git` и структура в ней). Также создается файл `.gitignore` (список файлов, которые не должны быть добавлены в репозиторий) 
```bash
git init
git branch -M main
git config user.name "Z0rinSerg"
git config user.email "sr.z0rs@gmail.com"
git remote add origin git@github.com:Z0rinSerg/ai_engineer_preproject.git
```

### Синхронизация локальной системы с облачной 

```bash
git pull
```

## Создание виртуального окружения 


```bash
uv init --name ai_engineer_preproject --python 3.12
```
Создались необходимые папки и файлы для виртуального окружения, папки для кода, файл `pyproject.toml` для управления проектом  т.д.

добавим еще нужных папок в структуры проекта:

```bash
mkdir -p notebooks src/ai_engineer_preproject scripts
```


Теперь добавим в pyproject.toml зависимости, необходимые для работы с Jupyter и MCP-серверами, а также настроим VSCode. 

```bash
uv add jupyterlab ipython fastmcp
```

Настроим VSCode. Чтобы ноутбуки и код использовали созданное uv-окружение:
```bash
mkdir -p .vscode && cat > .vscode/settings.json << 'EOF'
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "notebook.kernelSources": [
        {
            "name": "ai_engineer_preproject (uv)",
            "path": "${workspaceFolder}/.venv/bin/python"
        }
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/.mypy_cache": true,
        "**/.pytest_cache": true,
        "**/.ipynb_checkpoints": true
    }
}
EOF
```

установим зависимости:
```bash
uv sync
```
Теперь зафиксируем это изменение в Git и проверим статус репозитория:
```bash
git add pyproject.toml
git commit -m "fix: migrate uv dev-dependencies to dependency-groups"
git status
```
Репозиторий на github создавался "руками". 
Настройка доступа по ssh (также потребует создание SSH-ключей и добавление их в настройки репозитория - здесь не приводятся подробно): 


Пушим из терминала:
```bash
git push -u origin main
```
В дальнейшем коммитим и пушим из интерфейса VS Code. 

# Собираем среду дальше для урока
Это установит все библиотеки, необходимые для курса: ~~requests~~ `httpx`, `numpy`, `sentence-transformers`, `faiss-cpu` и `pypdf`.
```bash
uv add numpy sentence-transformers faiss-cpu pypdf httpx
uv sync
```