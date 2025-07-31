from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models import MetaData, insert_metadata, delete_metadata
import os
import boto3
import sqlite3
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS setup
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


@app.get("/")
def root():
    return {"message": "🚀 Google Drive Clone running!"}


@app.get("/view")
def list_files():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        file_list = [item['Key'] for item in response.get('Contents', [])]
        return file_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Upload to S3
        s3.upload_fileobj(file.file, BUCKET_NAME, file.filename)

        metadata = MetaData(
            filename=file.filename,
            size=file.size or 0,
            headers=dict(file.headers),
            content_type=file.content_type,
            upload_time=datetime.now().isoformat()
        )

        insert_metadata(metadata)
        return {"message": f"{file.filename} uploaded successfully ✅"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {e}")


@app.get("/download/{filename}")
def generate_download_link(filename: str):
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": filename},
            ExpiresIn=3600
        )
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {e}")


@app.delete("/delete/{filename}")
def delete_file(filename: str):
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
        delete_metadata(filename)
        return {"message": f"{filename} deleted ✅"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete error: {e}")