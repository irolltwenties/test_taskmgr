from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from repos.gateway import DatabaseGateway
from config.cfg import Configuration
from tests.mocks.factory import FakeRepositoryFactory


class FakeGateway(DatabaseGateway):
    def __init__(self, config: Configuration):
        self._config = config
        self._engine = None
        self._session_factory = None
        self._is_initialized = True

    async def initialize(self):
        pass

    async def close(self):
        pass

    @asynccontextmanager
    async def session(self):
        yield None

    def get_repository_factory(self, session: AsyncSession):
        return FakeRepositoryFactory(session)
