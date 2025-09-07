import uuid

from models.dto import TaskDTO
from models.requests import TaskCreateRequest, TaskUpdateRequest


class FakeData:
    @staticmethod
    def get_valid_task_data() -> TaskDTO:
        return TaskDTO(
            id=uuid.uuid4(), name="another_test", text="another_test", status="created"
        )

    @staticmethod
    def get_valid_create_task_request() -> TaskCreateRequest:
        return TaskCreateRequest(
            name="another_test", text="another_test", status="created"
        )

    @staticmethod
    def get_valid_update_request() -> TaskUpdateRequest:
        return TaskUpdateRequest(
            name="another_test_updated",
            text="another_test_updated",
            status="processing",
        )

    @staticmethod
    def get_invalid_create_request() -> dict:
        return {"name": "test-wrong", "status": "created"}

    @staticmethod
    def get_empty_create_request() -> dict:
        return {"name": "", "text": "", "status": "created"}

    @staticmethod
    def get_wrong_status_request() -> dict:
        return {
            "name": "valid_name",
            "text": "valid_text",
            "status": "non_existent_status",  # Несуществующий статус
        }
