"""Init tasks data

Revision ID: 92f541263972
Revises: e7dd09506a28
Create Date: 2025-09-05 00:38:27.084578

"""

from datetime import datetime, timezone
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy import column, table
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "92f541263972"
down_revision: Union[str, Sequence[str], None] = "e7dd09506a28"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем объект таблицы для работы с данными
    tasks_table = table(
        "tasks",
        column("id", sa.UUID),
        column("name", sa.String),
        column("text", sa.String),
        column("status", sa.String),
        column("created_at", sa.DateTime),
        column("updated_at", sa.DateTime),
        column("deleted_at", sa.DateTime),
    )

    # Данные для вставки
    initial_tasks = [
        {
            "id": uuid4(),
            "name": "Изучить FastAPI",
            "text": "Освоить основы FastAPI и создать простое API",
            "status": "created",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "deleted_at": None,
        },
        {
            "id": uuid4(),
            "name": "Настроить базу данных",
            "text": "Подключить PostgreSQL и настроить миграции с Alembic",
            "status": "created",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "deleted_at": None,
        },
        {
            "id": uuid4(),
            "name": "Реализовать аутентификацию",
            "text": "Добавить JWT аутентификацию с Bearer токенами",
            "status": "created",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "deleted_at": None,
        },
        {
            "id": uuid4(),
            "name": "Написать тесты",
            "text": "Создать unit и integration tests для API",
            "status": "created",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "deleted_at": None,
        },
        {
            "id": uuid4(),
            "name": "Деплой приложения",
            "text": "Развернуть приложение на сервере с Docker",
            "status": "created",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "deleted_at": None,
        },
    ]

    # Вставляем данные
    op.bulk_insert(tasks_table, initial_tasks)


def downgrade() -> None:
    # Удаляем все добавленные задачи (очищаем таблицу)
    op.execute("DELETE FROM tasks")
    # ### end Alembic commands ###
