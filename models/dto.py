import datetime
import uuid
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class TaskDTO(BaseModel):
    """
    Data Transfer Object для задачи.

    Attributes:
        id: UUID задачи
        name: Название задачи (1-1000 символов, не пустое)
        text: Текст задачи (1-1000 символов, не пустое)
        status: Статус задачи: created, processing или done
    """

    id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=1000, pattern=r"^.*\S.*$")
    text: str = Field(..., min_length=1, max_length=1000, pattern=r"^.*\S.*$")
    status: Literal["created", "processing", "done"]
    # created_at: datetime.datetime

    class Config:
        from_attributes = True

    @field_validator("text", "name")
    def validate_text_not_empty(cls, v):
        if not v or v.isspace():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()
