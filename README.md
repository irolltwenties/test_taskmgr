# TASK MANAGER API

A RESTful API for a task management system built with FastAPI and PostgreSQL.
Allows managing tasks through HTTP requests (GET, POST, PUT, DELETE).
Swagger documentation is available after application startup.

## Technologies

- FastAPI - web framework
- PostgreSQL - database
- SQLAlchemy 2.0 - ORM
- Alembic - migrations
- Docker - containerization
- Pydantic - data validation

## Requirements

- Docker and Docker Compose
- Working PostgreSQL
- Configured .env file

## Installation

Clone the repository:
```bash
git clone https://github.com/irolltwenties/test_taskmgr.git
```

# Setup

## Update .env file

Create or update the `.env` file based on [.env.example](.env.example) file.

## Update Alembic configuration

Update the `alembic.ini` file with the following database URL format:
```ini
sqlalchemy.url = postgresql+psycopg2://${TEST_QUEST_DB_LOGIN}:${TEST_QUEST_DB_PASSWORD}@${TEST_QUEST_DB_HOST}:${TEST_QUEST_DB_PORT}/${TEST_QUEST_DB_NAME}
```
**Note:** While the application uses asyncpg, Alembic prefers synchronous drivers, hence psycopg2-binary is used (included in requirements.txt).

# Running with Docker Compose

Start all services in detached mode:
```bash
docker compose up -d
```
View application logs:
```bash
docker compose logs -f <container name or id>
```

## Alternative run (no container)
Remark: you would not need to setup .env file for this way,
but you still need to setup alembic.ini to run migrations

### Create virtual environment
Linux:
```bash
python3 -m venv .venv
```
Windows:
```commandline
py -m venv venv
```
or
```commandline
python -m venv venv
```
### Activate virtual environment
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
After that you must see .venv (or venv) mark left to your directory in terminal.
### Install dependencies
```shell
pip install -r requirements.txt
```
### Apply migrations
```bash
alembic upgrade head
```
### Try to start
Linux:
```bash
python3 main.py
```
Windows:
```commandline
py main.py
```
or 
```commandline
python main.py
```

# API Documentation

After application startup, documentation is available at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Ensure port 8000 is exposed from the Docker container to access the documentation.

# Running Tests

Run tests with coverage:
```bash
docker compose exec <container_id> pytest --cov
```
# Testing with Postman

Import the collection from: `TEST_TASKMGR_API.postman_collection.json`

# Troubleshooting

## Database Connection Errors

Ensure that:
- PostgreSQL container is running (`docker-compose ps`)
- .env file variables are correct
- Network ports are not occupied

## Migration Errors

Try restarting migrations:
```bash
docker compose exec <container_id> alembic downgrade base
docker compose exec <container_id> alembic upgrade head
```

# other languages readme
readme is also available on russian language [README-ru.md](README-ru.md)