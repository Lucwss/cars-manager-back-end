from fastapi import status, HTTPException, Path, Query, APIRouter, Request, Body
from typing import Optional, List
from src.models.pydantic_models.car.car_db import CarDB
from src.models.pydantic_models.car.car_base import CarBase
from src.models.pydantic_models.car.car_update import CarUpdate
from src.utils.parsers.car_parsers import CarParser
from fastapi.responses import JSONResponse
from src.controllers.car_controller import CarController

cars_router = APIRouter()


@cars_router.get("/", status_code=status.HTTP_208_ALREADY_REPORTED, response_description='List all cars')
async def list_all_cars(request: Request,
                        min_price: int = Query(0),
                        max_price: int = Query(100000),
                        brand: Optional[str] = Query(None),
                        page: int = Query(1)) -> List[CarDB]:
    all_cars: List[CarDB] = await CarController.list_all_cars(request=request,
                                                              min_price=min_price,
                                                              max_price=max_price,
                                                              brand=brand, page=page)
    return all_cars


@cars_router.post("/", status_code=status.HTTP_201_CREATED, response_description="Add new car")
async def create_car(request: Request, car: CarBase = Body(...)):
    if created_car := await CarController.create_car(request=request, car=car):
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@cars_router.get("/{id}", status_code=status.HTTP_200_OK, response_description="get a single car")
async def get_car_by_id(request: Request, id: str = Path(...)):
    if (car := await CarController.get_car_by_id(request=request, id=id)) is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=CarParser.parse_car(car))
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Car with id {id} not found")


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