import folium
from folium.plugins import MarkerCluster
from typing import List
import os
import uuid
from app.schemas.markers import MapPoint


# --- SRP: Extracted helper functions ---
from typing import Optional


def build_popup(marker: MapPoint) -> Optional[folium.Popup]:
    """
    Builds a styled Bootstrap popup for a given map marker.

    Args:
        marker (MapPoint): A map point that may contain label, description,
                           and an optional URL button.

    Returns:
        Optional[folium.Popup]: A folium popup if there is any content,
                                otherwise None.
    """
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
    """
    Adds a single marker to the given MarkerCluster, with an optional popup.

    Args:
        marker (MapPoint): The map point data to render on the map.
        cluster (MarkerCluster): The cluster to which the marker will be added.
    """
    popup = build_popup(marker)
    folium.Marker(location=(marker.lat, marker.lon), popup=popup).add_to(cluster)


def create_map(markers: List[MapPoint]) -> folium.Map:
    """
    Initializes a Folium map and adds clustered markers.

    Args:
        markers (List[MapPoint]): A list of MapPoint instances to plot on the map.

    Returns:
        folium.Map: A map object containing the clustered markers.
    """
    if not markers:
        raise ValueError("Markers list cannot be empty")
    base = folium.Map(location=(markers[0].lat, markers[0].lon), zoom_start=12)
    cluster = MarkerCluster().add_to(base)
    for marker in markers:
        add_marker_to_cluster(marker, cluster)
    return base


def save_map_to_static(map_obj: folium.Map) -> str:
    """
    Saves the given map object as an HTML file in the static/maps directory.

    Args:
        map_obj (folium.Map): The Folium map object to save.

    Returns:
        str: A relative URL path to the saved HTML file for browser access.
    """
    STATIC_MAPS_DIR = "static/maps"
    os.makedirs(STATIC_MAPS_DIR, exist_ok=True)
    file_name = f"{uuid.uuid4().hex}.html"
    file_path = os.path.join(STATIC_MAPS_DIR, file_name)
    map_obj.save(file_path)
    return f"/static/maps/{file_name}"


def generate_map(markers: List[MapPoint]) -> str:
    """
    Generates an HTML map with markers and saves it in static/maps.

    This is the main entry point for map creation, orchestrating the process of
    rendering, clustering, and exporting.

    Args:
        markers (List[MapPoint]): List of map points with optional
                                  label, description, and button.

    Returns:
        str: Public URL path to the generated HTML file.
    """
    map_obj = create_map(markers)
    return save_map_to_static(map_obj)
