from unittest.mock import AsyncMock

from repos.factory import RepositoryFactory


def test_repository_factory_creation():
    mock_gateway = AsyncMock()
    factory = RepositoryFactory(mock_gateway)

    assert hasattr(factory, "tasks")

    repo = factory.tasks
    assert repo is not None
    assert callable(repo.get_all)
