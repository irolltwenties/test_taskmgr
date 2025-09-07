import uuid
from typing import Protocol, TypeVar, Generic, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from models.dto import TaskDTO


T = TypeVar("T")
ID = TypeVar("ID", int, str, uuid.UUID)


class IRepository(Protocol[T, ID]):
    """Base repo interface"""

    async def get_by_id(self, id: ID) -> Optional[T]: ...

    async def get_all(self) -> list[T]: ...

    async def create(self, entity: T | Dict) -> T: ...

    async def update(self, task_id: ID, update_data: Dict) -> T: ...

    async def delete(self, id: ID) -> bool: ...


class ITasksRepository(IRepository[TaskDTO, uuid.UUID], Protocol):
    # could skip this cause no special methods here
    pass


class BaseRepository(Generic[T, ID]):

    def __init__(self, session: AsyncSession, model: type[T]):
        self._session = session
        self._model = model
