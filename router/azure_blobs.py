from fastapi import APIRouter, Depends, File, UploadFile, HTTPException,Form
from fastapi.responses import JSONResponse
import os
from io import BytesIO
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient,BlobSasPermissions,generate_blob_sas
from pathlib import Path
from pydantic import BaseModel
from .basic_import import is_authenticated

router = APIRouter()

def azure_connection():
    # from env take AZURE_STORAGE_CONNECTION_STRING
    connect_string = "DefaultEndpointsProtocol=https;AccountName=gsmstore;AccountKey=tKc6zDb61jnf7GSHQWwX6S5Uz83twOtNczf6GUhq/1S0mBixn/Qx2Mwh6QibQSSYaKv/iRd2zS24+AStTtOf5g==;EndpointSuffix=core.windows.net"
    # createing connecction for azure blob
    blob_service_client = BlobServiceClient.from_connection_string(connect_string)
    # return blob 
    return blob_service_client

async def create_container(content:bytes = None,file_name:str=None,location:str=None):
    try:
        blob_service_client = azure_connection()
        container_client = blob_service_client.get_container_client(container=location)
        blob_name = f"{file_name}"
        blob_client = container_client.get_blob_client(blob=blob_name)
        blob_client.upload_blob(content, overwrite=True)
        return blob_client.url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to Azure Blob Storage: {e}")

# FastAPI route for file upload
@router.post("/upload_file/")
async def upload_file(file: UploadFile,location:str=Form(...),current_user: str = Depends(is_authenticated)):
    try:
        content = file.file.read()
        file_name = file.filename
        url = await create_container(content = content,file_name = file_name,location = location)
        return JSONResponse({"url":url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to Azure Blob Storage: {e}")