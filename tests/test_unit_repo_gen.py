import uuid
from typing import get_type_hints
from repos.tasks import TasksRepository
from repos.interface import ITasksRepository
from models.dto import TaskDTO


def test_repository_method_signatures():
    repo = TasksRepository

    # check ITasksRepository methods
    expected_methods = ["get_all", "get_by_id", "create", "update", "delete"]

    for method_name in expected_methods:
        assert hasattr(repo, method_name), f"Method {method_name} not implemented"

        repo_method = getattr(repo, method_name)
        assert callable(repo_method), f"Method {method_name} is not callable"


def test_method_signatures_compatibility():
    repo = TasksRepository

    repo_method = getattr(repo, "get_by_id")
    type_hints = get_type_hints(repo_method)

    assert "task_id" in type_hints or "id" in type_hints
    param_type = type_hints.get("task_id") or type_hints.get("id")
    assert param_type == uuid.UUID

    return_type = type_hints.get("return")
    assert return_type is not None

    if hasattr(return_type, "__args__"):
        # Union[TaskDTO, None]
        assert TaskDTO in return_type.__args__
    else:
        # TaskDTO
        assert return_type == TaskDTO


def test_repository_creates_task_dto_instances():
    repo_class = TasksRepository

    create_method = getattr(repo_class, "create")
    return_annotation = get_type_hints(create_method).get("return")

    assert (
        return_annotation == TaskDTO
    ), f"create should return TaskDTO, got {return_annotation}"


def test_interface_methods_exist():
    repo = TasksRepository

    interface_methods = [
        method
        for method in dir(ITasksRepository)
        if not method.startswith("_") and callable(getattr(ITasksRepository, method))
    ]

    for method_name in interface_methods:
        assert hasattr(
            repo, method_name
        ), f"Interface method {method_name} not implemented in repository"
        assert callable(
            getattr(repo, method_name)
        ), f"Method {method_name} is not callable"
