# TASK MANAGER API

RESTful API для системы управления задачами, построенный на FastAPI и PostgreSQL.
Позволяет управлять задачами через HTTP-запросы (GET, POST, PUT, DELETE).
Документация Swagger доступна после запуска приложения.

## Стек

- FastAPI - веб-фреймворк
- PostgreSQL - база данных
- SQLAlchemy 2.0 - ORM
- Alembic - миграции
- Docker - контейнеризация
- Pydantic - валидация

## Требования

- Docker и Docker Compose
- Запущенный PostgreSQL
- Настроенный .env файл и alembic.ini.

## Установка

Клонируйте репозиторий:
```bash
git clone https://github.com/irolltwenties/test_taskmgr.git
```

# Настройка и пуск приложения

## Обновить .env файл

Создайте или обновите `.env` файл на основе файла [.env.example](.env.example).

## Обновить конфигурацию alembic

Обновите файл `alembic.ini`, установив значение sqlalchemy.url, соответствующее вашим кредам базы данных:
```ini
sqlalchemy.url = postgresql+psycopg2://${TEST_QUEST_DB_LOGIN}:${TEST_QUEST_DB_PASSWORD}@${TEST_QUEST_DB_HOST}:${TEST_QUEST_DB_PORT}/${TEST_QUEST_DB_NAME}
```
**Заметка:** Хотя приложение использует asyncpg, Alembic требует синхронный драйвер, поэтому используется psycopg2-binary (см. requirements.txt).

# Запуск через docker-compose

Старт сервиса:
```bash
docker compose up -d
```
Смотрим логи:
```bash
docker compose logs -f <container name or id>
```

## Альтернативно: запуск без контейнера
Пометка: 
Хотя вам не потребуется .env файл в этом случае (все можно задать как энвы через export или хардкодом в config/cfg.py),
но все равно потребуется настроить alembic.ini.

### Создаем виртуальное окружение
Linux:
```bash
python3 -m venv .venv
```
Windows:
```commandline
py -m venv venv
```
или
```commandline
python -m venv venv
```
### Активируем виртуальное окружение
Linux:
```bash
cd .venv/bin && source activate && cd ../../
```
Windows:
```commandline
cd venv/scripts
```
```commandline
activate
```
```commandline
cd ../../
```
Убедитесь, что в терминале появилась надпись venv (.venv) слева от директории.
### Устанавливаем зависимости
```shell
pip install -r requirements.txt
```
### Применяем миграции
Для этого должен быть прописан dsn в alembic.ini (ссылка формата postgresql+psycopg2)
```bash
alembic upgrade head
```
### Пробуем запустить
Linux:
```bash
python3 main.py
```
Windows:
```commandline
py main.py
```
или 
```commandline
python main.py
```

# Документация API

После старта приложения, документация доступна по ссылкам:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Ссылка может изменяться в зависимости от хоста и порта апи (локалхост+8000 это дефолт для разработки)

# Запуск тестов

Запуск тестов с coverage (82%):
```bash
docker compose exec <container_id> pytest --cov
```
# Тестируем с Postman

Вы можете импортировать готовую для тестовых сценариев коллекцию запросов Postman.
[TEST_TASKMGR_API.postman_collection.json](TEST_TASKMGR_API.postman_collection.json)

# Траблшутинг

## Ошибки подключения к базе данных

Убедитесь, что:
- PostgreSQL запущен локально или удаленно
- .env файл прописан верно
- Постулируемые порты не заняты чем-то еще

## Ошибки при миграциях

Проверьте файл alembic.ini (вы должны завести туда креды своей бд), попробуйте рестартнуть миграции:
```bash
docker compose exec <container_id> alembic downgrade base
docker compose exec <container_id> alembic upgrade head
```

