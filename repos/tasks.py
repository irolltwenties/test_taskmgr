import uuid
from datetime import datetime
from typing import Dict
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.dto import TaskDTO
from models.orm import TaskORM
from repos.interface import BaseRepository, ITasksRepository


class TasksRepository(BaseRepository[TaskDTO, int], ITasksRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TaskDTO)

    async def get_all(self) -> list[TaskDTO]:
        result = await self._session.execute(select(TaskORM))
        orm_objects = result.scalars().all()
        return [TaskDTO.model_validate(orm_obj) for orm_obj in orm_objects]

    async def get_by_id(self, task_id: uuid.UUID) -> TaskDTO | None:
        result = await self._session.execute(
            select(TaskORM).where(TaskORM.id == task_id)
        )
        orm_obj = result.scalar_one_or_none()
        return TaskDTO.model_validate(orm_obj) if orm_obj else None

    async def create(self, task_data: dict) -> TaskDTO:
        if "id" not in task_data or not task_data["id"]:
            task_data["id"] = uuid.uuid4()
        orm_obj = TaskORM(**task_data)
        self._session.add(orm_obj)
        await self._session.flush()
        await self._session.refresh(orm_obj)
        return TaskDTO.model_validate(orm_obj)

    async def update(self, task_id: UUID, update_data: Dict) -> TaskDTO:
        """
        Partial update of task - only provided fields are updated
        """
        # Проверяем существование задачи
        existing_task = await self.get_by_id(task_id)
        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found",
            )

        # Валидация - хотя бы одно поле должно быть передано для обновления
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update",
            )

        # Создаем временный DTO для валидации данных
        # Используем существующие данные + новые данные для обновления
        validation_data = existing_task.model_dump()
        validation_data.update(update_data)

        try:
            # Валидируем объединенные данные
            TaskDTO(**validation_data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Validation error: {e}"
            )

        # Обновляем запись в базе
        stmt = (
            update(TaskORM)
            .where(TaskORM.id == task_id)
            .values(**update_data, updated_at=datetime.utcnow())
            .returning(TaskORM)
        )

        result = await self._session.execute(stmt)
        updated_orm = result.scalar_one()

        await self._session.flush()
        await self._session.refresh(updated_orm)

        return TaskDTO.model_validate(updated_orm)

    async def delete(self, task_id: uuid.UUID) -> bool:
        # check existence
        task = await self.get_by_id(task_id)
        if not task:
            # need to do something to move server-like logics
            # like 404 err up the stack to the fastapi app
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found",
            )

        result = await self._session.execute(
            delete(TaskORM).where(TaskORM.id == task_id)
        )
        await self._session.flush()
        return result.rowcount > 0
