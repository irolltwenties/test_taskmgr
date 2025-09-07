from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class TaskCreateRequest(BaseModel):

    name: str = Field(..., min_length=1, max_length=1000, pattern=r"^.*\S.*$")
    text: str = Field(..., min_length=1, max_length=1000, pattern=r"^.*\S.*$")
    status: Literal["created", "processing", "done"] = "created"

    @field_validator("text", "name")
    def validate_text_not_empty(cls, v):
        if not v or v.isspace():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()


class TaskUpdateRequest(BaseModel):
    """Model to request task update"""

    name: Optional[str] = Field(
        None, min_length=1, max_length=1000, pattern=r"^.*\S.*$"
    )
    text: Optional[str] = Field(
        None, min_length=1, max_length=1000, pattern=r"^.*\S.*$"
    )
    status: Optional[Literal["created", "processing", "done"]] = None

    @field_validator("text", "name")
    def validate_text_not_empty(cls, v):
        if v is not None:
            if not v or v.isspace():
                raise ValueError("Text cannot be empty or whitespace only")
            return v.strip()
        return v

    def dict(self, exclude_unset=True, exclude_none=True, **kwargs):
        return super().model_dump(
            exclude_unset=exclude_unset, exclude_none=exclude_none, **kwargs
        )
