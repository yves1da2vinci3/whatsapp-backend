from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from app.utils.minio_client import upload_to_minio, get_bucket_objects

router = APIRouter(prefix="/upload")

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    bucket_name: str = "default-bucket"
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
    page_size: int = 100
):
    try:
        objects_generator = get_bucket_objects(bucket_name, page_size=page_size)
        objects = list(objects_generator)
        
        if not objects:
            return JSONResponse(content={"message": "No objects found in the bucket"}, status_code=404)

        total_pages = len(objects)

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