from pydantic import BaseModel, Field


class InsertCar(BaseModel):
    brand: str = Field(...)
    model: str = Field(...)
    year: int = Field(...)
