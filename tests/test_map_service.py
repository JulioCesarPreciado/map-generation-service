import pytest
from app.services.map import generate_map
import os
from app.schemas.markers import MapPoint


def test_generate_map_creates_file():
    markers = [
        MapPoint(lat=20.6736, lon=-103.344, label="Centro"),
        MapPoint(lat=20.6765, lon=-103.347, label="Templo Expiatorio")
    ]
    public_path = generate_map(markers)
    # Convert the public path to the real file system path
    file_path = os.path.join("static/maps", os.path.basename(public_path))
    assert os.path.exists(file_path)
    assert file_path.endswith(".html")


def test_generate_map_empty_input():
    with pytest.raises(ValueError):
        generate_map([])
