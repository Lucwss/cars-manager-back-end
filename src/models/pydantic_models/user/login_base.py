from pydantic import BaseModel
from pydantic import EmailStr, Field


class LoginBase(BaseModel):
    email: EmailStr = EmailStr(...)
    password: str = Field(...)
