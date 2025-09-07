from unittest.mock import AsyncMock

from fastapi import Depends

from app.core import App
from logger.simple import configure_logger
from config.cfg import Configuration
from tests.mocks.factory import FakeRepositoryFactory
from tests.mocks.gateway import FakeGateway


class FakeApp(App):
    def __init__(self, config: Configuration):
        self._logger = configure_logger("test-uvicorn-app")
        self._bearer = config.task_mgr_bearer
        self.gateway = FakeGateway(config)
        self._app = self._create_fastapi_app()
        self._setup_routes()
        self._setup_auth_middleware()

    # @staticmethod
    # def get_repository_factory(gateway: FakeGateway):
    #     def factory_dependency():
    #         return gateway.get_repository_factory(AsyncMock())
    #
    #     return Depends(factory_dependency)

    def get_repository_factory(self, gateway: FakeGateway) -> FakeRepositoryFactory:
        return gateway.get_repository_factory(AsyncMock())
