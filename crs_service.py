import re
from typing import Optional

def determine_measurement_crs(source_crs: Optional[str]) -> Optional[str]:
    """Return a suitable projected CRS for measurement calculations.

    The function accepts the source CRS identifier (e.g., "EPSG:4326")
    and returns a CRS that is appropriate for planar measurements.
    Simple heuristic:
    * If the source CRS is geographic (latitude/longitude), default to
      Web Mercator (EPSG:3857) which is a common projected CRS.
    * If the source CRS is already projected (contains a numeric EPSG code
      that is not 4326), return it unchanged.
    * If the CRS is unknown or ``None``, return ``None`` so callers can
      decide how to handle the missing information.
    """
    if not source_crs:
        return None
    crs = source_crs.strip().upper()
    # If EPSG:4326 or any geographic EPSG (4xxx), use Web Mercator
    if crs == "EPSG:4326" or re.match(r"^EPSG:4[0-9]{3}$", crs):
        return "EPSG:3857"
    return crs
