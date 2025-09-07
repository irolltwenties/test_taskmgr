import uuid
from typing import List, Optional
from models.dto import TaskDTO


class FakeTasksRepository:

    _shared_storage = {}

    def __init__(self):
        self._initialize_with_data()

    def _initialize_with_data(self):
        if not self._shared_storage:
            tasks = [
                {"name": "test1", "text": "test1", "status": "created"},
                {"name": "test2", "text": "test2", "status": "created"},
                {"name": "test3", "text": "test3", "status": "created"},
            ]

            for task_data in tasks:
                task_id = uuid.uuid4()  # Генерируем UUID вместо integer
                task = TaskDTO(id=task_id, **task_data)
                self._shared_storage[task_id] = task

    async def get_all(self) -> List[TaskDTO]:
        return list(self._shared_storage.values())

    async def get_by_id(
        self, task_id: uuid.UUID
    ) -> Optional[TaskDTO]:  # Меняем тип на UUID
        return self._shared_storage.get(task_id)

    async def update(self, task_id: uuid.UUID, task_data: dict) -> Optional[TaskDTO]:
        if task_id not in self._shared_storage:
            return None

        existing_task = self._shared_storage[task_id]
        updated_task = TaskDTO(
            id=task_id,
            name=task_data.get("name", existing_task.name),
            text=task_data.get("text", existing_task.text),
            status=task_data.get("status", existing_task.status),
        )
        self._shared_storage[task_id] = updated_task
        return updated_task

    async def create(self, task_data: dict) -> TaskDTO:
        task_id = uuid.uuid4()
        task = TaskDTO(
            id=task_id,
            name=task_data["name"],
            text=task_data["text"],
            status=task_data["status"],
        )
        self._shared_storage[task_id] = task
        return task

    async def delete(self, task_id: uuid.UUID) -> bool:
        if task_id in self._shared_storage:
            del self._shared_storage[task_id]
            return True
        return False

    async def get_any_id_if_exists(self) -> uuid.UUID | None:
        all_rows = await self.get_all()
        return all_rows[0].id if all_rows else None

    @classmethod
    def reset_storage(cls):
        cls._shared_storage.clear()
