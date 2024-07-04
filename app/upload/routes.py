from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from minio import Minio
from dotenv import load_dotenv
import os
import tempfile
from app.utils.minio_client import upload_to_minio, get_bucket_objects

load_dotenv()

router = APIRouter()

def get_minio_client():
    return Minio(
        "localhost:9000",
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False,
    )

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    bucket_name: str = "default-bucket",
):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        object_name = file.filename
        uploaded_path = upload_to_minio(temp_file_path, bucket_name, object_name)

        os.unlink(temp_file_path)

        return JSONResponse(
            content={"message": "File uploaded successfully", "path": uploaded_path},
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{bucket_name}")
async def list_bucket_objects(
    bucket_name: str,
    page: int = 1,
    page_size: int = 100,
    minio_client: Minio = Depends(get_minio_client)
):
    try:
        objects = list(get_bucket_objects(minio_client, bucket_name, page_size=page_size))
        total_pages = len(objects)

        if not objects:
            return JSONResponse(content={"message": "No objects found in the bucket"}, status_code=404)

        if page < 1 or page > total_pages:
            raise HTTPException(status_code=400, detail="Invalid page number")

        return JSONResponse(
            content={
                "objects": objects[page - 1],
                "page": page,
                "total_pages": total_pages,
                "page_size": page_size,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))