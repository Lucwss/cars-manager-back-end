from src.models.pydantic_models.mongo.mongo_base_model import MongoBaseModel
from pydantic import Field


class CarBase(MongoBaseModel):
    brand: str = Field(..., min_length=3)
    make: str = Field(..., min_length=3)
    year: int = Field(...)
    price: float = Field(...)
    km: int = Field(...)
    cm3: int = Field(...)
