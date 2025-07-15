import os
import uuid
from fastapi import UploadFile
from typing import Literal
from pathlib import Path
from dotenv import load_dotenv
from app.config import config
import boto3

# import cloudinary
# import cloudinary.uploader

load_dotenv()

class FileUploadHandler:
    def __init__(self):
        self.storage_type: Literal["local", "s3", "cloudinary"] = config.FILE_STORAGE_TYPE
        self.bucket_name = config.AWS_S3_BUCKET
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=config.AWS_S3_REGION,
        )

        # cloudinary.config(
        #     cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        #     api_key=os.getenv("CLOUDINARY_API_KEY"),
        #     api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        #     secure=True
        # )

    async def upload_file(self, file: UploadFile, folder: str = "general") -> str:
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        if self.storage_type == "local":
            return await self._save_locally(file, folder, filename)
        elif self.storage_type == "s3":
            return await self._upload_to_s3(file, folder, filename)
        elif self.storage_type == "cloudinary":
            return await self._upload_to_cloudinary(file, folder)
        else:
            raise ValueError("Unsupported storage type")

    async def _save_locally(self, file: UploadFile, folder: str, filename: str) -> str:
        folder_path = Path("static/uploads") / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        return f"/static/uploads/{folder}/{filename}"

    async def _upload_to_s3(self, file: UploadFile, folder: str, filename: str) -> str:
        key = f"{folder}/{filename}"
        content = await file.read()
        self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=content)
        url = f"https://{self.bucket_name}.s3.{os.getenv('AWS_S3_REGION')}.amazonaws.com/{key}"
        return url

    async def _upload_to_cloudinary(self, file: UploadFile, folder: str) -> str:
        # content = await file.read()
        # result = cloudinary.uploader.upload(content, folder=folder)
        # return result["secure_url"]
        pass
