from fastapi import Request, Query
from typing import Optional, List
from src.models.pydantic_models.car.car_db import CarDB
from src.models.pydantic_models.car.car_base import CarBase
from src.models.pydantic_models.car.car_update import CarUpdate
from fastapi.encoders import jsonable_encoder


class CarController:
    @staticmethod
    async def list_all_cars(request: Request, min_price: int = Query(0), max_price: int = Query(100000),
                            brand: Optional[str] = Query(None),
                            page: int = Query(1)) -> List[CarDB]:
        results_per_page = 25
        skip = (page - 1) * results_per_page
        query = {"price": {"$gt": min_price, "$lt": max_price}}

        if brand:
            query["brand"] = brand

        full_query = request.app.mongo.database()['cars1'].find(query).sort("_id", -1).skip(skip).limit(
            results_per_page)

        results = [CarDB(**raw_car) async for raw_car in full_query]

        # this is also possible
        # results = await full_query.to_list(1000
        return results

    @staticmethod
    async def create_car(request: Request, car: CarBase):
        car = jsonable_encoder(car)
        new_car = await request.app.mongo.database()['cars1'].insert_one(car)
        created_car = await request.app.mongo.database()['cars1'].find_one({"_id": new_car.inserted_id})
        return created_car

    @staticmethod
    async def get_car_by_id(request: Request, id: str):
        if (car := await request.app.mongo.database()['cars1'].find_one({"_id": id})) is not None:
            return CarDB(**car)

    @staticmethod
    async def update_car(request: Request, id: str, car: CarUpdate):
        await request.app.mongo.database()['cars1'].update_one({"_id": id}, {"$set": car.dict(exclude_unset=True)})
        if (updated_car := await request.app.mongo.database()['cars1'].find_one({"_id": id})) is not None:
            return CarDB(**updated_car)

    @staticmethod
    async def delete_car(request: Request, id: str) -> bool:
        delete_result = await request.app.mongo.database()['cars1'].delete_one({"_id": id})
        if delete_result.deleted_count == 1:
            return True
        return False

