import json
from typing import List
from shapely.geometry import shape
from app.storage.metadata_store import MetadataStore
from app.schemas.file_schema import FeatureMeasurement

class MeasurementService:
    """Service to calculate measurements for features of an uploaded file."""

    def __init__(self):
        self.metadata_store = MetadataStore()

    async def calculate_measurements(self, file_id: str, skip: int = 0, limit: int = 100) -> List[FeatureMeasurement]:
        meta = self.metadata_store.get(file_id)
        if not meta:
            raise Exception(f"Metadata for file_id {file_id} not found")
        features = meta.get("features", [])
        measurement_crs = meta.get("measurement_crs")
        # Pagination
        paged = features[skip : skip + limit]
        results: List[FeatureMeasurement] = []
        for f in paged:
            geom_geojson = f.get("geometry")
            if geom_geojson is None:
                # Should not happen, but guard
                continue
            geom = shape(geom_geojson)
            geom_type = f.get("geometry_type")
            area_sqm = None
            area_hectares = None
            length_m = None
            length_km = None
            warnings = []
            if geom_type in ("Polygon", "MultiPolygon"):
                try:
                    area_sqm = geom.area
                    area_hectares = area_sqm / 10000.0
                except Exception as e:
                    warnings.append(str(e))
            elif geom_type in ("LineString", "MultiLineString"):
                try:
                    length_m = geom.length
                    length_km = length_m / 1000.0
                except Exception as e:
                    warnings.append(str(e))
            elif geom_type in ("Point", "MultiPoint"):
                # No measurement needed
                pass
            else:
                warnings.append(f"Unsupported geometry type: {geom_type}")
            fm = FeatureMeasurement(
                feature_id=f.get("feature_id"),
                geometry_type=geom_type,
                geometry_coordinates=geom_geojson,
                attributes=f.get("properties"),
                area_sqm=area_sqm,
                area_hectares=area_hectares,
                length_m=length_m,
                length_km=length_km,
                status="COMPLETED" if not warnings else "WARNINGS",
                warnings=warnings if warnings else None,
            )
            results.append(fm)
        return results
