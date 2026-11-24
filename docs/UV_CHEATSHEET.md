# Справочник по `uv`

Краткое руководство по управлению Python-проектами с помощью `uv`. Держать под рукой на столе.

## 0. Установка и обновление `uv`

```sh
# быстрый способ
curl -LsSf https://astral.sh/uv/install.sh | sh

# более контролируемый способ: скачать релиз и проверить контрольную сумму
wget https://releases.astral.sh/github/uv/releases/download/0.13.5/uv-x86_64-unknown-linux-gnu.tar.gz
wget https://releases.astral.sh/github/uv/releases/download/0.13.5/uv-x86_64-unknown-linux-gnu.tar.gz.sha256

sha256sum --check uv-x86_64-unknown-linux-gnu.tar.gz.sha256

tar -xvzf uv-x86_64-unknown-linux-gnu.tar.gz --strip-components=1 -C ~/.local/bin
```

## 1. Управление версиями Python

```sh
uv python install 3.12           # установить версию (скачивается готовая сборка)
uv python pin 3.12               # зафиксировать версию проекта → .python-version
uv python list --only-installed  # список установленных версий
uv run --python 3.11 python -V   # разовый запуск на другой версии, uv скачает её автоматически
```

## 2. Виртуальные окружения

```sh
uv venv                  # создать .venv
uv run python app.py     # запустить команду в окружении проекта
```

`uv run` сам подготавливает окружение — отдельно активировать `.venv` не нужно.

## 3. Инициализация проекта

```sh
# ничего лишнего, только pyproject.toml
uv init --bare my_bare_proj

# минимальный набор файлов для запускаемого проекта, например CLI
uv init --app my_app

# минимальный набор файлов для библиотеки
uv init --lib my_lib

# если пакет не нужно собирать как wheel или sdist
uv init --app --no-package my_webapp
```

## 4. Управление зависимостями

`uv add` добавляет зависимости в проект (под капотом вызывает ещё `uv lock` и `uv sync`):

```sh
# основные зависимости
uv add fastapi uvicorn==0.52.4

# dev-зависимости
uv add --group=dev ruff mypy

# опциональные зависимости
uv add --group=optional mkdocs

# кастомные индексы
uv add flash-attn --index astral-cu128=https://wheels.astral.sh/simple/cu128/

# удаление зависимостей
uv remove fastapi
uv remove --group=dev mypy
```

## 5. Lock-файл: `uv lock`

Обновляет проектный lock-файл (под капотом вызывает ещё `uv sync`):

```sh
uv lock                              # создать/обновить uv.lock
uv lock --upgrade                    # обновить все пакеты в lock-файле
uv lock --upgrade-package uvicorn    # обновить конкретный пакет
uv lock --dry-run --upgrade          # посмотреть потенциальные изменения без применения
uv lock --script fetch.py            # залочить зависимости standalone-скрипта
```

## 6. Синхронизация окружения: `uv sync`

Синхронизирует окружение с lock-файлом, при необходимости обновляет его:

```sh
uv sync                  # синхронизация из дефолтных групп (default-groups в pyproject.toml)
uv sync --group=optional # синхронизация конкретной группы
uv sync --frozen         # без резолва и обновления uv.lock
uv sync --locked         # упадёт, если pyproject.toml не соответствует uv.lock
uv sync --dry-run        # показать потенциальные изменения

# в Docker: установить всё, кроме самого проекта
uv sync --locked --no-install-project

# в Docker: установить сам проект как неперемещаемый пакет
uv sync --frozen --no-editable
```

**Разница между `--locked` и `--frozen`:**

| Флаг | Поведение при расхождении pyproject.toml и uv.lock | Сценарий |
|---|---|---|
| `--locked` | команда падает | CI — поймать забытый незакоммиченный uv.lock |
| `--frozen` | просто ставится то, что в uv.lock | Docker-сборки, резолв не нужен |

## 7. Standalone-скрипты со встроенными зависимостями (PEP 723)

Зависимости описываются инлайн прямо в файле скрипта:

```sh
# создать скрипт с инлайн-зависимостями
uv init --script fetch.py --python 3.13.3

# добавить инлайн-зависимости в скрипт
uv add --script fetch.py requests rich

# окружение соберётся само и скрипт запустится
uv run --script fetch.py

# можно залочить версии зависимостей для лучшей воспроизводимости
uv lock --script fetch.py
```

## 8. Drop-in режимы `uv pip` (совместим с pip и pip-tools)

Удобен для постепенного перевода проекта на `uv` или работы в чужом проекте без `uv`-структуры.

Как замена `pip`:

```sh
uv pip install requests "fastapi[standard]"
uv pip install -r requirements.txt
```

Как замена `pip-tools`:

```sh
# разрезолвить конкретные версии зависимостей
uv pip compile requirements.in -o requirements.txt

# обновить конкретный пакет на новую совместимую версию
uv pip compile --upgrade-package requests requirements.in -o requirements.txt

# полная синхронизация зависимостей текущего окружения
uv pip sync requirements.txt
```

## 9. Инструменты (`uv tool` / `uvx`)

```sh
uv tool install ruff           # постоянная установка утилиты
uv tool run pycowsay 'Hello!'  # разовый запуск утилиты без установки
uv tool upgrade --all          # обновить все установленные утилиты
uv tool list                   # список установленных утилит

# uvx — алиас uv tool run
uvx ruff check .               # разовый запуск во временном окружении
uvx ruff@0.6.0 check .         # конкретная версия, без установки
```

## 10. Работа в чужом проекте

Если проект использует `uv`, весь бутстрап — одна команда:

```sh
git clone ... && cd project
uv run pytest
```

Если проект не на `uv`, достаточно разово:

```sh
uv venv
uv pip install -e . --group tests
uv run pytest
```

## 11. `uv` в Docker

### Получение бинаря

Бинарь берут из отдельного образа, не собирая внутри:

```Dockerfile
COPY --from=docker.io/astral/uv:0.13.6 /uv /uvx /bin/
```

### Управление через переменные окружения

У каждой переменной есть парный флаг (например, `UV_PYTHON_DOWNLOADS=0` равносильно `--no-python-downloads`), но переменные удобнее — не дублируют флаги запуска:

```Dockerfile
# не устанавливать Python через uv, использовать системный
ENV UV_PYTHON_DOWNLOADS=0
# компилировать байткод пакетов при их установке
ENV UV_COMPILE_BYTECODE=1
# чтобы uv не ругался на разные файловые системы при использовании кеша
ENV UV_LINK_MODE=copy
# не устанавливать dev-зависимости
ENV UV_NO_DEV=1
```

### Промежуточные слои и монтирование кеша

Чтобы не перекачивать внешние зависимости при изменении кода, первым слоем ставят внешние зависимости, а потом копируют код приложения. Кеш монтируется, а не копируется в образ — при небольшом изменении uv.lock `uv` берёт почти всё из кеша и скачивает только новое, а образ остаётся легковесным:

```Dockerfile
WORKDIR /app

# устанавливаем в окружение внешние зависимости
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# копируем код приложения
COPY . /app

# устанавливаем в окружение сам проект (если он устанавливаемый)
RUN uv sync --frozen --no-editable
```

### Multi-stage, если в финальном образе не нужны бинари `uv`

```Dockerfile
# сборочный стейдж, в котором есть uv
FROM docker.io/python:3.14-slim AS builder

COPY --from=docker.io/astral/uv:0.13.6 /uv /uvx /bin/

# команды, которым нужен uv или uvx
# ...

# финальный стейдж без бинарей uv
FROM docker.io/python:3.14-slim

# команды, которым uv уже не нужен
# ...
```

### Сборка и запуск образа

```sh
cd my_webapp
docker build -t otus-webapp:v0.0.1 .

# проверка содержимого
docker run --rm -it --entrypoint bash otus-webapp:v0.0.1

# запуск
docker run --rm --publish 8080:80 otus-webapp:v0.0.1 \
    --app-dir src my_webapp.app:app --host=0.0.0.0 --port 80

# проверка с хоста
curl -X 'GET' 'http://127.0.0.1:8080/health'
```

## 12. Мини-шпаргалка

| Задача | Команда |
|---|---|
| Установить Python | `uv python install 3.12` |
| Зафиксировать версию Python | `uv python pin 3.12` |
| Создать проект | `uv init --app` / `--lib` / `--bare` |
| Создать окружение | `uv venv` (или вообще ничего — `uv run`) |
| Добавить зависимость | `uv add X` |
| Удалить зависимость | `uv remove X` |
| Залочить версии | `uv lock` / `uv pip compile` |
| Обновить пакет | `uv lock --upgrade-package X` |
| Синхронизировать окружение | `uv sync` / `uv pip sync` |
| Установить CLI-утилиту | `uv tool install X` |
| Разово запустить утилиту | `uvx X` |
| Запустить скрипт с инлайн-зависимостями | `uv run --script` |
| Запустить код проекта | `uv run` |
