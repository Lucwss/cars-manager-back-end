from fastapi import APIRouter
from fastapi import Header

headers_router = APIRouter()


@headers_router.get('/headers')
async def read_headers(user_agent: str | None = Header(None)):
    return {
        "User-Agent": user_agent
    }
