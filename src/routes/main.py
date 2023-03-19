from fastapi import APIRouter
from src.routes.car_routes.index import cars_router
from src.routes.upload_files.index import upload_file_route
from src.routes.headers.index import headers_router
from src.routes.account.index import account_router

main_router = APIRouter()
main_router.include_router(router=cars_router, prefix='/cars')
main_router.include_router(router=upload_file_route, prefix='/file')
main_router.include_router(router=headers_router, prefix='/get')
main_router.include_router(router=account_router)


@main_router.get("/")
async def root():
    return {'message': 'welcome to this fantastic app'}


@main_router.post("/")
async def post_root():
    return {"message": "Post request success"}
