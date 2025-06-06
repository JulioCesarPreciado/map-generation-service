import folium
from folium.plugins import MarkerCluster
from typing import List, Tuple
import os
import uuid


def generate_map(markers: List[Tuple[float, float]]) -> str:
    """
    Generates an HTML map with markers.

    Args:
        markers (List[Tuple[float, float]]):
        A list of tuples containing latitude and longitude.

    Returns:
        str: Path to the generated HTML file.
    """
    if not markers:
        raise ValueError("Markers list cannot be empty")

    STATIC_MAPS_DIR = "static/maps"
    os.makedirs(STATIC_MAPS_DIR, exist_ok=True)

    map_obj = folium.Map(location=markers[0], zoom_start=12)
    cluster = MarkerCluster().add_to(map_obj)

    for lat, lon in markers:
        folium.Marker(location=(lat, lon)).add_to(cluster)

    file_name = f"{uuid.uuid4().hex}.html"
    file_path = os.path.join(STATIC_MAPS_DIR, file_name)
    map_obj.save(file_path)

    return f"/static/maps/{file_name}"
