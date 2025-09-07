from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager

from config.cfg import Configuration


class DatabaseGateway:
    """Class to manage all conns and repos"""

    def __init__(self, config: Configuration):
        self._config = config
        self._engine = None
        self._session_factory = None
        self._is_initialized = False

    async def initialize(self):
        """init on app start"""
        if self._is_initialized:
            return

        self._engine = create_async_engine(
            f"postgresql+asyncpg://{self._config.db_login}:{self._config.db_password}@"
            f"{self._config.db_host}:{self._config.db_port}/{self._config.db_name}",
            echo=True,
            pool_size=20,
            max_overflow=20,
        )

        self._session_factory = async_sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )

        self._is_initialized = True
        print("DatabaseGateway initialized")

    async def close(self):
        """when app closes"""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None
            self._is_initialized = False
        print("DatabaseGateway closed")

    @asynccontextmanager
    async def session(self):
        """session context manager"""
        if not self._is_initialized:
            await self.initialize()

        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
