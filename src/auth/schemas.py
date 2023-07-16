# pydantic models
import uuid
from pydantic import EmailStr

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    email: EmailStr
    is_superuser: bool
    is_verified: bool


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    email: EmailStr
