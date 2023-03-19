from src.models.pydantic_models.mongo.mongo_base_model import MongoBaseModel
from typing import Optional


class CarUpdate(MongoBaseModel):
    price: Optional[int] = None
