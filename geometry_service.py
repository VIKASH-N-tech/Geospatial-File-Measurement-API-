import geopandas as gpd
from shapely.geometry.base import BaseGeometry
from typing import List, Tuple, Optional

def extract_features(data_path: str) -> Tuple[List[dict], Optional[str]]:
    """Extract geospatial features from a Shapefile or KML.

    Args:
        data_path: Path to the .shp file or .kml file.
    Returns:
        A tuple containing a list of feature dictionaries and the source CRS string.
        Each feature dictionary includes:
            - "feature_id": int index
            - "geometry": shapely geometry object
            - "properties": dict of attribute values
    """
    # GeoPandas can read both Shapefile and KML (via fiona driver)
    gdf = gpd.read_file(data_path)
    # Determine source CRS identifier
    source_crs = None
    if gdf.crs:
        source_crs = f"EPSG:{gdf.crs.to_epsg()}" if gdf.crs.to_epsg() else str(gdf.crs)
    else:
        source_crs = None

    features: List[dict] = []
    for idx, row in gdf.iterrows():
        geometry: BaseGeometry = row.geometry
        # Remove geometry column to get properties
        properties = row.drop(labels=["geometry"]).to_dict()
        features.append({
            "feature_id": int(idx),
            "geometry": geometry,
            "properties": properties,
        })
    return features, source_crs
