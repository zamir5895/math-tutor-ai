from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

import os
from dotenv import load_dotenv
from  typing import Optional
import uuid

from dotenv import dotenv_values

env_vars = dotenv_values(".env")
print(env_vars["REGION"])
print(env_vars["BUCKET_NAME"])
print(env_vars["ACCESS_KEY_ID"])
print(env_vars["SECRET_ACCESS_KEY"])
print(env_vars["SESSION_TOKEN"])
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('SESSION_TOKEN'),
    region_name=os.getenv('REGION'),
)


def upload_file_to_s3(file: UploadFile, bucket: str, s3_key: str) -> bool:
    try:
        

        s3_client.upload_fileobj(
            file.file,
            bucket,
            s3_key,
            ExtraArgs={
                'ContentType': file.content_type
            }
        )

        print(f"Archivo subido a S3: {s3_key}")
        return True
    except NoCredentialsError:
        print("Credenciales no disponibles")
        return False
    except Exception as e:
        print(f"Error al subir archivo: {e}")
        return False



@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), folder: Optional[str] = None):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    else:
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        s3_key = f"{folder}/{unique_filename}" if folder else unique_filename
    
        if upload_file_to_s3(file, os.getenv('BUCKET_NAME'), s3_key):
            location = s3_client.get_bucket_location(Bucket=os.getenv('BUCKET_NAME'))['LocationConstraint']
            url = f"https://{os.getenv('BUCKET_NAME')}.s3.{location}.amazonaws.com/{s3_key}"
            
            return {
                "message": "Archivo subido exitosamente",
                "filename": file.filename,
                "s3_key": s3_key,
                "url": url,
                "content_type": file.content_type
            }
        else:
            raise HTTPException(status_code=500, detail="Error al subir el archivo a S3")

@app.get("/")
def read_root():
    return {"message": "API para subir archivos a S3"}