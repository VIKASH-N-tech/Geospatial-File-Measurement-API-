import os
import uuid
import shutil
import tempfile
from typing import List
# pyrefly: ignore [missing-import]
from fastapi import UploadFile
from app.storage.metadata_store import MetadataStore
from app.config import settings
from app.services.geometry_service import extract_features
# pyrefly: ignore [missing-import]
from app.services.crs_service import determine_measurement_crs

class FileService:
    """Service handling file storage and initial processing."""

    def __init__(self):
        self.metadata_store = MetadataStore()
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    async def save_upload(self, file_id: str, upload_file: UploadFile) -> str:
        """Save the uploaded file to the uploads directory.
        Returns the absolute path to the saved file.
        """
        ext = os.path.splitext(upload_file.filename)[1].lower()
        dest_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
        # Write file content
        with open(dest_path, "wb") as out_file:
            content = await upload_file.read()
            out_file.write(content)
        return dest_path

    async def process_file(self, file_id: str, file_path: str):
        """Extract features, determine CRS, and save metadata.
        Returns a dict representing the stored metadata.
        """
        ext = os.path.splitext(file_path)[1].lower()
        # Use a temporary directory for extraction when handling zip files
        with tempfile.TemporaryDirectory() as tmp_dir:
            if ext == ".zip":
                # Secure extraction to avoid path traversal
                import zipfile
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    for member in zip_ref.namelist():
                        # Prevent absolute paths or ".." navigation
                        member_path = os.path.normpath(member)
                        if ".." in member_path.split(os.path.sep) or os.path.isabs(member_path):
                            raise Exception("Unsafe file path in zip archive")
                    zip_ref.extractall(tmp_dir)
                # Find the .shp file inside extracted folder
                shp_files = []
                for root, _, files in os.walk(tmp_dir):
                    for f in files:
                        if f.lower().endswith('.shp'):
                            shp_files.append(os.path.join(root, f))
                if not shp_files:
                    raise Exception("No .shp file found in the uploaded zip archive")
                data_path = shp_files[0]
            elif ext == ".kml":
                data_path = file_path
            else:
                raise Exception("Unsupported file extension")

            # Extract features using geometry_service
            features, source_crs = extract_features(data_path)
            # Convert geometry objects to GeoJSON for JSON-serializable storage
            from shapely.geometry import mapping
            serializable_features = []
            for f in features:
                geom = f["geometry"]
                serializable_features.append({
                    "feature_id": f["feature_id"],
                    "geometry_type": geom.geom_type,
                    "geometry": mapping(geom),
                    "properties": f["properties"],
                })
            features = serializable_features

        # Determine measurement CRS (projected) based on source CRS
        measurement_crs = determine_measurement_crs(source_crs)

        metadata = {
            "id": file_id,
            "original_filename": os.path.basename(file_path),
            "file_format": ext.lstrip('.'),
            "upload_timestamp": None,  # will be set by caller (FastAPI uses datetime)
            "feature_count": len(features),
            "source_crs": source_crs,
            "measurement_crs": measurement_crs,
            "status": "COMPLETED",
            "error_details": None,
            "features": features,  # store raw feature dicts for later measurement
        }
        # Save metadata
        self.metadata_store.set(file_id, metadata)
        return metadata

    async def get_metadata(self, file_id: str):
        """Retrieve stored metadata for a given file ID."""
        meta = self.metadata_store.get(file_id)
        if not meta:
            return None
        # Convert upload_timestamp to datetime if not set
        from datetime import datetime
        if meta.get("upload_timestamp") is None:
            meta["upload_timestamp"] = datetime.utcnow()
            self.metadata_store.set(file_id, meta)
        return meta
