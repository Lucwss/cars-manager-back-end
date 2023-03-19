from fastapi import status, HTTPException, Path, Query, APIRouter, Request, Body
from typing import Optional, List
from src.models.pydantic_models.car.car_db import CarDB
from src.models.pydantic_models.car.car_base import CarBase
from src.models.pydantic_models.car.car_update import CarUpdate
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

cars_router = APIRouter()


@cars_router.get("/", status_code=status.HTTP_208_ALREADY_REPORTED, response_description='List all cars')
async def list_all_cars(request: Request,
                        min_price: int = Query(0),
                        max_price: int = Query(100000),
                        brand: Optional[str] = Query(None),
                        page: int = Query(1)) -> List[CarDB]:
    pass
    results_per_page = 25
    skip = (page - 1) * results_per_page
    query = {"price": {"$gt": min_price, "$lt": max_price}}

    if brand:
        query["brand"] = brand

    full_query = request.app.mongo.database()['cars1'].find(query).sort("_id", -1).skip(skip).limit(results_per_page)

    results = [CarDB(**raw_car) async for raw_car in full_query]

    # this is also possible
    # results = await full_query.to_list(1000
    return results


@cars_router.post("/", status_code=status.HTTP_201_CREATED, response_description="Add new car")
async def create_car(request: Request, car: CarBase = Body(...)):
    car = jsonable_encoder(car)
    new_car = await request.app.mongo.database()['cars1'].insert_one(car)
    created_car = await request.app.mongo.database()['cars1'].find_one({"_id": new_car.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)


@cars_router.get("/{id}", status_code=status.HTTP_200_OK, response_description="get a single car")
async def get_car_by_id(request: Request, id: str = Path(...)):
    if (car := await request.app.mongo.database()['cars1'].find_one({"_id": id})) is not None:
        return CarDB(**car)
    raise HTTPException(status_code=404, detail=f"Car with id {id} not found")


@cars_router.put("/{id}", response_description="update car")
async def update_car(request: Request, id: str = Path(...), car: CarUpdate = Body(...)):
    await request.app.mongo.database()['cars1'].update_one({"_id": id}, {"$set": car.dict(exclude_unset=True)})
    if (car := await request.app.mongo.database()['cars1'].find_one({"_id": id})) is not None:
        return CarDB(**car)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with {id} not found")


@cars_router.delete("/{id}", response_description="delete car")
async def delete_car(request: Request, id: str = Path(...)):
    delete_result = await request.app.mongo.database()['cars1'].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with {id} not found")


@cars_router.get("/cars-request/info")
async def raw_request(request: Request):
    return {
        "message": request.base_url,
        "query": request.query_params,
        "headers": request.headers,
        "cookies": request.cookies,
        "body": request.body,
        "client": request.client,
        "close": request.close,
        "get": request.get,
        "is_disconnected": request.is_disconnected,
        "items": request.items,
        "json": request.json,
        "method": request.method,
        "path_params": request.path_params,
        "query_params": request.query_params,
        "receive": request.receive,
        "send_push_promise": request.send_push_promise,
        "stream": request.stream,
        "url": request.url,
    }