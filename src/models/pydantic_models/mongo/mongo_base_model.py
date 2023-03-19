from pydantic import BaseModel, Field
from src.models.bson.py_object_id import PyObjectId
from bson import ObjectId


class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        