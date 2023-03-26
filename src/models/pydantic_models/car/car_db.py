from src.models.pydantic_models.car.car_base import CarBase
from pydantic import Field


class CarDB(CarBase):
    owner: str = Field(...)
