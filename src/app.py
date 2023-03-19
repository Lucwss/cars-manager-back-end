from fastapi import FastAPI
from src.routes.main import main_router
from fastapi.middleware.cors import CORSMiddleware
from src.database.mongo import Mongo

import uvicorn

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_up_db_client():
    app.mongo = Mongo()
    app.mongo_client = app.mongo.connection
    app.mongo_database = app.mongo.database()


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo = Mongo()
    app.mongo_client = app.mongo.connection
    app.mongo_client.close()

app.include_router(router=main_router, prefix='/app')

if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000)
