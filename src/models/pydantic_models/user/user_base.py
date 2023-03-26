from src.models.pydantic_models.mongo.mongo_base_model import MongoBaseModel
from pydantic import Field
from src.enums.role import Role
from email_validator import EmailNotValidError, validate_email
from pydantic import validator, EmailStr


class UserBase(MongoBaseModel):
    username: str = Field(..., min_length=3, max_length=15)
    email: str = Field(...)
    password: str = Field(...)
    role: Role

    @validator("email")
    def valid_email(cls, v):
        try:
            email = validate_email(v).email
            return email
        except EmailNotValidError as e:
            raise EmailNotValidError
