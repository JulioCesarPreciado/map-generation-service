import folium
from folium.plugins import MarkerCluster
from typing import List, Tuple
from tempfile import NamedTemporaryFile


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

    map = folium.Map(location=markers[0], zoom_start=12)
    cluster = MarkerCluster().add_to(map)

    for lat, lon in markers:
        folium.Marker(location=(lat, lon)).add_to(cluster)

    with NamedTemporaryFile(
        suffix='.html',
        delete=False,
        mode='w',
        encoding='utf-8'
    ) as tmp:
        map.save(tmp.name)
        return tmp.name
