from pydantic import BaseModel
from pydantic import EmailStr, Field


class CurrentUser(BaseModel):
    email: EmailStr = EmailStr(...)
    username: str = Field(...)
    role: str = Field(...)
