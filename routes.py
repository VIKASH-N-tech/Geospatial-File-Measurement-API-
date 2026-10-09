# pyrefly: ignore [missing-import]
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from typing import List, Optional
from datetime import datetime
import uuid
import os

from app.schemas.file_schema import FileMetadata, FileUploadResponse, MeasurementResponse, FeatureMeasurement
# pyrefly: ignore [missing-import]
from app.services.file_service import FileService
# pyrefly: ignore [missing-import]
from app.services.measurement_service import MeasurementService

router = APIRouter()

file_service = FileService()
measurement_service = MeasurementService()

@router.post("/files/", response_model=FileUploadResponse, tags=["Files"])
async def upload_file(file: UploadFile = File(...)):
    # Validate extension
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in {".zip", ".kml"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    # Generate unique ID
    file_id = str(uuid.uuid4())
    # Save file to uploads directory
    try:
        saved_path = await file_service.save_upload(file_id, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Process file immediately (synchronous for simplicity)
    try:
        metadata = await file_service.process_file(file_id, saved_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return FileUploadResponse(
        id=metadata.id,
        filename=metadata.original_filename,
        feature_count=metadata.feature_count,
        crs=metadata.source_crs,
        status=metadata.status,
        upload_timestamp=metadata.upload_timestamp,
    )

@router.get("/files/{file_id}/", response_model=FileMetadata, tags=["Files"])
async def get_file_info(file_id: str):
    metadata = await file_service.get_metadata(file_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="File not found")
    return metadata

@router.get("/files/{file_id}/measurements/", response_model=MeasurementResponse, tags=["Measurements"])
async def get_measurements(
    file_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    metadata = await file_service.get_metadata(file_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="File not found")
    features = await measurement_service.calculate_measurements(file_id, skip, limit)
    return MeasurementResponse(
        file_id=file_id,
        measurement_crs=metadata.measurement_crs,
        features=features,
    )
