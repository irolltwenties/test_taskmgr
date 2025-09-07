import pytest
from fastapi.testclient import TestClient
from tests.mocks.appcore import FakeApp
from tests.mocks.cfg import FakeConfiguration
from tests.mocks.data import FakeData


class TestHighLevelLogicsComplex:
    @pytest.fixture(scope="class")
    def config(self):
        return FakeConfiguration()

    @pytest.fixture(scope="class")
    def app(self, config):
        return FakeApp(config)

    @pytest.fixture(scope="class")
    def headers(self, config):
        return {"Authorization": f"Bearer {config.task_mgr_bearer}"}

    @pytest.fixture(scope="class")
    def client(self, app):
        with TestClient(app.app) as test_client:
            yield test_client

    @pytest.mark.asyncio
    async def test_get_all(self, client, headers, app):
        """Test getting initial tasks"""
        response = client.get("/tasks/", headers=headers)
        assert response.status_code == 200
        initial_tasks = response.json()
        assert len(initial_tasks) == 3

    @pytest.mark.asyncio
    async def test_get(self, client, headers, app):
        """Test getting a specific task by ID"""
        some_id = await app.get_repository_factory(
            app.gateway
        ).tasks.get_any_id_if_exists()
        response = client.get(f"/tasks/{some_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["id"] == str(some_id)

    @pytest.mark.asyncio
    async def test_create(self, client, headers):
        fake_data = FakeData.get_valid_create_task_request()
        response = client.post("/tasks/", headers=headers, json=fake_data.model_dump())
        assert response.status_code == 201
        result = response.json()
        assert result["text"] == fake_data.text
        assert result["name"] == fake_data.name
        assert result["status"] == fake_data.status

    @pytest.mark.asyncio
    async def test_update(self, client, headers, app):
        """Test updating an existing task"""
        some_id = await app.get_repository_factory(
            app.gateway
        ).tasks.get_any_id_if_exists()
        task = await app.get_repository_factory(app.gateway).tasks.get_by_id(some_id)
        fake_data = FakeData.get_valid_update_request()
        fake_data_json = fake_data.model_dump()
        fake_data_json["id"] = str(some_id)  # uuid is not serializable
        response = client.put(f"/tasks/{some_id}", headers=headers, json=fake_data_json)
        assert response.status_code == 200
        result = response.json()
        assert result["text"] == fake_data.text != task.text
        assert result["name"] == fake_data.name != task.name
        assert result["status"] == fake_data.status != task.status

    @pytest.mark.asyncio
    async def test_delete(self, client, headers):
        """Test deleting a task"""
        fake_data = FakeData.get_valid_create_task_request()
        create_response = client.post(
            "/tasks/", headers=headers, json=fake_data.model_dump()
        )
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        response = client.delete(f"/tasks/{task_id}", headers=headers)
        assert response.status_code == 200

        response = client.get(f"/tasks/{task_id}", headers=headers)
        print(response.json())
        assert response.status_code == 200 and not response.json()

    @pytest.mark.asyncio
    async def test_task_structure(self, client, headers, app):
        """Test that task has expected structure"""
        some_id = await app.get_repository_factory(
            app.gateway
        ).tasks.get_any_id_if_exists()
        response = client.get(f"/tasks/{some_id}", headers=headers)
        assert response.status_code == 200

        task = response.json()
        assert "id" in task
        assert "name" in task
        assert "text" in task
        assert "status" in task

    @pytest.mark.asyncio
    async def test_create_wrong(self, client, headers):
        """Test creating task with invalid data structure"""

        response = client.post(
            "/tasks/", headers=headers, json=FakeData.get_invalid_create_request()
        )
        assert response.status_code == 422

        error_detail = response.json()
        assert "detail" in error_detail
        assert any("text" in str(error).lower() for error in error_detail["detail"])

    @pytest.mark.asyncio
    async def test_create_empty_string(self, client, headers):
        """Test creating task with empty required fields"""
        response = client.post(
            "/tasks/", headers=headers, json=FakeData.get_empty_create_request()
        )
        assert response.status_code in [400, 422, 500]

    @pytest.mark.asyncio
    async def test_update_to_empty_string(self, client, headers, app):
        """Test updating task with empty fields"""
        some_id = await app.get_repository_factory(
            app.gateway
        ).tasks.get_any_id_if_exists()

        response = client.put(
            f"/tasks/{some_id}",
            headers=headers,
            json=FakeData.get_empty_create_request(),
        )
        assert response.status_code in [400, 422, 500]

    @pytest.mark.asyncio
    async def test_wrong_update(self, client, headers, app):
        """Test updating with invalid status value"""
        some_id = await app.get_repository_factory(
            app.gateway
        ).tasks.get_any_id_if_exists()
        response = client.put(
            f"/tasks/{some_id}",
            headers=headers,
            json=FakeData.get_wrong_status_request(),
        )
        assert response.status_code in [400, 422, 500]

    @pytest.mark.asyncio
    async def test_delete_missing_task(self, client, headers):
        """Test deleting non-existent task"""
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        response = client.delete(f"/tasks/{non_existent_id}", headers=headers)
        assert response.status_code == 404

        error_detail = response.json()
        assert "detail" in error_detail
        assert "not found" in error_detail["detail"].lower()

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client):
        """Test accessing endpoints without authorization"""
        # Test without headers
        response = client.get("/tasks/")
        assert response.status_code == 401

        response = client.get("/tasks/some-id")
        assert response.status_code == 401

        response = client.post("/tasks/", json={})
        assert response.status_code == 401

        response = client.put("/tasks/some-id", json={})
        assert response.status_code == 401

        response = client.delete("/tasks/some-id")
        assert response.status_code == 401

        # Test with wrong token
        wrong_headers = {"Authorization": "Bearer wrong_token"}
        response = client.get("/tasks/", headers=wrong_headers)
        assert response.status_code == 401
