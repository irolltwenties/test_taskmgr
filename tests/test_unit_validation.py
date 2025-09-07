import pytest
from pydantic import ValidationError
from models.dto import TaskDTO
from models.requests import TaskCreateRequest


def test_task_dto_validation():
    # Valid data
    task = TaskDTO(
        id="123e4567-e89b-12d3-a456-426614174000",
        name="Test",
        text="Description",
        status="created",
    )
    assert task.name == "Test"

    # Invalid status
    with pytest.raises(ValidationError):
        TaskDTO(
            id="123e4567-e89b-12d3-a456-426614174000",
            name="Test",
            text="Description",
            status="invalid_status",
        )


def test_task_create_request_validation():
    task = TaskCreateRequest(name="Test", text="Description", status="created")
    assert task.name == "Test"

    # Missing required field
    with pytest.raises(ValidationError):
        TaskCreateRequest(
            name="Test",
            # text missing
            status="created",
        )
