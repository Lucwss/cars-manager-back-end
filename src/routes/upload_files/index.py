from fastapi import APIRouter
from fastapi import Form, File, UploadFile
import shutil

upload_file_route = APIRouter()


@upload_file_route.post('/upload')
async def upload(file: UploadFile = File(...), brand: str = Form(...), model: str = Form(...)):
    with open('saved_file.png', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "brand": brand,
        "model": model,
        "file_name": file.filename
    }
