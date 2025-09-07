from sqlalchemy.ext.asyncio import AsyncSession

from repos.interface import ITasksRepository
from repos.tasks import TasksRepository


class RepositoryFactory:
    def __init__(self, session: AsyncSession):
        self.__tasks = TasksRepository(session)

    @property
    def tasks(self) -> ITasksRepository:
        return self.__tasks
