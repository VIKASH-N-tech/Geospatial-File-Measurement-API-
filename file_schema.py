# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class FileMetadata(BaseModel):
    """Metadata stored for each uploaded file."""
    id: str = Field(..., description="Unique identifier for the file")
    original_filename: str = Field(..., description="Name of the file as uploaded by the client")
    file_format: str = Field(..., description="File format (zip or kml)")
    upload_timestamp: datetime = Field(..., description="UTC timestamp of the upload")
    feature_count: int = Field(..., description="Number of geospatial features extracted")
    source_crs: Optional[str] = Field(None, description="CRS identifier of the source data (e.g., EPSG:4326)")
    measurement_crs: Optional[str] = Field(None, description="CRS used for measurement calculations")
    status: str = Field(..., description="Processing status – COMPLETED, FAILED, PENDING")
    error_details: Optional[str] = Field(None, description="Error message if processing failed")

class FileUploadResponse(BaseModel):
    """Response payload after a successful upload."""
    id: str
    filename: str
    feature_count: int
    crs: Optional[str]
    status: str
    upload_timestamp: datetime

class FeatureMeasurement(BaseModel):
    """Individual feature measurement entry returned by the measurements endpoint."""
    feature_id: int
    geometry_type: str
    geometry_coordinates: Optional[dict] = None
    attributes: Optional[dict] = None
    area_sqm: Optional[float] = None
    area_hectares: Optional[float] = None
    length_m: Optional[float] = None
    length_km: Optional[float] = None
    status: str = "COMPLETED"
    warnings: Optional[List[str]] = None

class MeasurementResponse(BaseModel):
    """Response payload for GET /files/{id}/measurements/"""
    file_id: str
    measurement_crs: Optional[str]
    features: List[FeatureMeasurement]
