import folium
from folium.plugins import MarkerCluster
from typing import List
import os
import uuid
from app.schemas.markers import MapPoint


# --- SRP: Extracted helper functions ---
from typing import Optional


def build_popup(marker: MapPoint) -> Optional[folium.Popup]:
    parts = []
    if marker.label:
        parts.append(f"<strong>{marker.label}</strong><br>")
    if marker.description:
        parts.append(f"<p>{marker.description}</p>")
    if marker.btnUrl:
        text = marker.btnText or "More"
        parts.append(
            (
                f'<a href="{marker.btnUrl}" target="_blank" '
                f'class="btn btn-primary text-white">{text}</a>'
            )
        )
    return folium.Popup("".join(parts), max_width=250) if parts else None


def add_marker_to_cluster(marker: MapPoint, cluster: MarkerCluster):
    popup = build_popup(marker)
    folium.Marker(location=(marker.lat, marker.lon), popup=popup).add_to(cluster)


def create_map(markers: List[MapPoint]) -> folium.Map:
    if not markers:
        raise ValueError("Markers list cannot be empty")
    base = folium.Map(location=(markers[0].lat, markers[0].lon), zoom_start=12)
    cluster = MarkerCluster().add_to(base)
    for marker in markers:
        add_marker_to_cluster(marker, cluster)
    return base


def save_map_to_static(map_obj: folium.Map) -> str:
    STATIC_MAPS_DIR = "static/maps"
    os.makedirs(STATIC_MAPS_DIR, exist_ok=True)
    file_name = f"{uuid.uuid4().hex}.html"
    file_path = os.path.join(STATIC_MAPS_DIR, file_name)
    map_obj.save(file_path)
    return f"/static/maps/{file_name}"


def generate_map(markers: List[MapPoint]) -> str:
    """
    Generates an HTML map with markers and saves it in static/maps.

    Args:
        markers (List[MapPoint]): List of map points with optional
        label, description, and button.

    Returns:
        str: Public URL path to the generated HTML file.
    """
    map_obj = create_map(markers)
    return save_map_to_static(map_obj)
