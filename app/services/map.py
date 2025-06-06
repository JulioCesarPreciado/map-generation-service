import folium
from folium.plugins import MarkerCluster
from typing import List
import os
import uuid
from app.schemas.markers import MapPoint


def generate_map(markers: List[MapPoint]) -> str:
    """
    Generates an HTML map with markers and saves it in static/maps.

    Args:
        markers (List[MapPoint]): List of map points with optional 
        label, description, and button.

    Returns:
        str: Public URL path to the generated HTML file.
    """
    if not markers:
        raise ValueError("Markers list cannot be empty")

    STATIC_MAPS_DIR = "static/maps"
    os.makedirs(STATIC_MAPS_DIR, exist_ok=True)

    map_obj = folium.Map(location=(markers[0].lat, markers[0].lon), zoom_start=12)
    cluster = MarkerCluster().add_to(map_obj)

    for marker in markers:
        popup_content = ""

        if marker.label:
            popup_content += f"<strong>{marker.label}</strong><br>"

        if marker.description:
            popup_content += f"<p>{marker.description}</p>"

        if marker.btnUrl:
            button_text = marker.btnText or "More"
            popup_content += (
                f'<a href="{marker.btnUrl}" target="_blank">'
                f'<button>{button_text}</button></a>'
            )

        if popup_content:
            popup = folium.Popup(popup_content, max_width=250)
            folium.Marker(location=(marker.lat, marker.lon), popup=popup).add_to(
                cluster
            )
        else:
            folium.Marker(location=(marker.lat, marker.lon)).add_to(cluster)

    file_name = f"{uuid.uuid4().hex}.html"
    file_path = os.path.join(STATIC_MAPS_DIR, file_name)
    map_obj.save(file_path)

    return f"/static/maps/{file_name}"
