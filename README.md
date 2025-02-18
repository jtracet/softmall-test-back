
## Начало работы

Для того чтобы выполнить описанные ниже команды, вам необходимо:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Для разработки

**ПРИМЕЧАНИЕ**: В проекте используется Python 3.11.

1. Установите [`poetry`](https://python-poetry.org/)
2. Установите зависимости:

```sh
poetry install
poetry shell
```

3. Установите pre-commit hooks: `pre-commit install`

Запустите контейнер с postgres: `docker compose up postgres`

4. Примените миграции:

```sh
alembic -c src/models/alembic.ini upgrade head
```

5. Выполните команду в консоле:

```sh
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Запуск тестов

```sh
pytest -v
```  


### Для работы в контейнере
```sh
docker compose up --build
```
  
