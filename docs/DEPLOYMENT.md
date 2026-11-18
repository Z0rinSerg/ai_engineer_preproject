# Описание (заметки) процесса создания среды разработки и анализа в проекте

## Создание папки проекта (если заново)
```bash
mkdir ai_engineer_preproject && cd ai_engineer_preproject
```

Дальше создадим виртуальное окружение. Оно изолирует библиотеки этого проекта от других проектов на вашем компьютере — зависимости не будут конфликтовать между собой. 

В моем случае - проект управляется uv и синхронизируется с GitHub. Описание действий ниже - это из описания урока на платформе Я.Практикум (ЯП). Оно не предусматривает использование uv, только pip для установки зависимостей даже recuirements не упомянут, venv в чистом виде и код в notebooks в jupyter. 
## Синхронизация с GitHub
### Первичная синхронизация в новой среде
```bash
git clone https://github.com/Z0rinSerg/ai_engineer_preproject
```

В моем случае создание в  папке проекта структуры проекта, в том числе папки для виртуального окружения и указанной версией python: 

```bash
uv init --name ai_engineer_preproject --python 3.12
```
добавим еще нужных папок в структуры проекта:

```bash
mkdir -p notebooks src/ai_engineer_preproject scripts
```

## Инициализация репозитория git и настройки для коммитов и синхронизации с GitHub. 

```bash
git init 
git config user.name "Z0rinSerg" 
git config user.email "z0rinserg@gmail.com"
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

```bash
git remote add origin git@github.com:Z0rinSerg/ai_engineer_preproject.git
```
Пушим из терминала:
```bash
git push -u origin main
```
В дальнейшем коммитим и пушим из интерфейса VS Code. 

Для Создания файлов формата Markdown в VS Code используется расширение Obsidian 
