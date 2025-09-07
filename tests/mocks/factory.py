from sqlalchemy.ext.asyncio import AsyncSession

from repos.factory import RepositoryFactory
from repos.interface import ITasksRepository
from tests.mocks.tasks_repo import FakeTasksRepository


class FakeRepositoryFactory(RepositoryFactory):

    def __init__(self, session: AsyncSession):
        self.__tasks = FakeTasksRepository()

    @property
    def tasks(self) -> ITasksRepository:
        # types are struggling here but the easiest way
        return self.__tasks
