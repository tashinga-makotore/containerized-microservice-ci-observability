from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=50,
    )

    status: Literal[
        "pending",
        "running",
        "complete",
    ] = "pending"

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned_name = value.strip()

        if not cleaned_name:
            raise ValueError("Task name cannot be empty")

        return cleaned_name