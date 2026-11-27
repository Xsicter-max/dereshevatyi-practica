from datetime import datetime
from pydantic import BaseModel, Field, field_validator
import re


USERNAME_PATTERN = re.compile(r"^[a-z0-9_]{3,32}$")


class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not USERNAME_PATTERN.match(v):
            raise ValueError(
                "username must contain only lowercase latin letters, digits and underscore, 3-32 chars"
            )
        return v


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}