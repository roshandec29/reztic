from fastapi import APIRouter, UploadFile, File, HTTPException, status, Form
from app.handlers.file_handler import FileUploadHandler

router = APIRouter(prefix="/api/v1/media", tags=["media"])
file_uploader = FileUploadHandler()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_image(
    folder: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload an image to the specified folder (locally or to S3 based on env).
    """
    try:
        image_url = await file_uploader.upload_file(file, folder)
        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image upload failed: {str(e)}"
        )
