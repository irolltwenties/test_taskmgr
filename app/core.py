from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Body, Request
from fastapi.responses import JSONResponse

from config.cfg import Configuration
from logger.simple import configure_logger
from models.requests import TaskUpdateRequest, TaskCreateRequest
from repos.factory import RepositoryFactory
from repos.gateway import DatabaseGateway


class App:
    """Класс-обертка для FastAPI приложения и агрегации нужных сущностей"""

    def __init__(self, configuration: Configuration):
        self._logger = configure_logger("uvicorn-app")
        self._bearer = configuration.task_mgr_bearer
        self.gateway = DatabaseGateway(configuration)
        self._app = self._create_fastapi_app()
        self._setup_routes()
        self._setup_auth_middleware()

    @property
    def app(self) -> FastAPI:
        return self._app

    def _create_fastapi_app(self) -> FastAPI:
        """create instance of fastapi app"""

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await self.gateway.initialize()
            yield
            await self.gateway.close()

        return FastAPI(
            title="TASKMGR API",
            description="API для менеджера задач",
            version="1.0.0",
            lifespan=lifespan,
        )

    def _setup_auth_middleware(self):
        """Setup authentication middleware"""

        @self.app.middleware("http")
        async def auth_middleware(request: Request, call_next):
            if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
                return await call_next(request)
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                self._logger.warning(
                    f"Missing Authorization header from {request.client.host}"
                )
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Authorization header missing"},
                    headers={"WWW-Authenticate": "Bearer"},
                )

            try:
                parts = auth_header.split()
                if len(parts) != 2:
                    print(len(parts))
                    print(parts)
                    print(auth_header)
                    raise ValueError("Invalid header format")

                scheme, token = parts
                if scheme.lower() != "bearer":
                    raise ValueError("Invalid authentication scheme")

                if token != self._bearer:
                    raise ValueError("Invalid token")

            except ValueError as e:
                self._logger.warning(
                    f"Invalid auth attempt from {request.client.host}: {e}"
                )
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid authentication credentials"},
                    headers={"WWW-Authenticate": "Bearer"},
                )

            self._logger.info(
                f"Authenticated request from {request.client.host} to {request.url.path}"
            )
            response = await call_next(request)
            return response

    def _setup_routes(self):
        """setup all endpoints routes"""
        router = APIRouter()

        @router.get("/tasks/", tags=["Tasks"])
        async def get_all_tasks(factory=self.get_repository_factory(self.gateway)):
            tasks = await factory.tasks.get_all()
            return tasks

        @router.get("/tasks/{task_id}", tags=["Tasks"])
        async def get_task(
            task_id: UUID, factory=self.get_repository_factory(self.gateway)
        ):
            task = await factory.tasks.get_by_id(task_id)
            return task

        @router.post("/tasks/", tags=["Tasks"], status_code=status.HTTP_201_CREATED)
        async def create_task(
            task_data: TaskCreateRequest = Body(...),
            factory=self.get_repository_factory(self.gateway),
        ):
            """
            Create a new task

            - **task_data**: Data for the new task
            """
            try:
                new_task = await factory.tasks.create(task_data.model_dump())
                return new_task
            except HTTPException as e:
                raise e
            except Exception as e:
                self._logger.error(f"Error creating task: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error",
                )

        @router.put("/tasks/{task_id}", tags=["Tasks"])
        async def update_task(
            task_id: UUID,
            update_request: TaskUpdateRequest = Body(...),
            factory=self.get_repository_factory(self.gateway),
        ):
            """
            Update task by ID

            - **task_id**: UUID of the task to update
            - **update_request**: Fields to update (all fields are optional)
            """
            try:
                update_data = update_request.model_dump(
                    exclude_unset=True, exclude_none=True
                )

                if not update_data:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No fields provided for update",
                    )

                updated_task = await factory.tasks.update(task_id, update_data)
                return updated_task

            except HTTPException as e:
                raise e
            except Exception as e:
                self._logger.error(f"Error updating task {task_id}: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error",
                )

        @router.delete("/tasks/{task_id}", tags=["Tasks"])
        async def delete_task(
            task_id: UUID,
            factory=self.get_repository_factory(self.gateway),
        ):
            """
            Delete task by ID

            - **task_id**: UUID of the task to delete
            """
            try:
                success = await factory.tasks.delete(task_id)
                if not success:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Task with id {task_id} not found",
                    )
                return {"message": f"Task {task_id} deleted successfully"}

            except HTTPException as e:
                raise e
            except Exception as e:
                self._logger.error(f"Error deleting task {task_id}: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error",
                )

        self.app.include_router(router)

    @staticmethod
    def get_repository_factory(gateway: DatabaseGateway) -> RepositoryFactory:
        async def _get_factory() -> RepositoryFactory:
            async with gateway.session() as session:
                factory = RepositoryFactory(session)
                yield factory

        return Depends(_get_factory)
