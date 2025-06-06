import pytest
from app.services.map import generate_map
import os


def test_generate_map_creates_file():
    markers = [(19.4326, -99.1332), (20.6597, -103.3496)]
    public_path = generate_map(markers)
    # Convert the public path to the real file system path
    file_path = os.path.join("static/maps", os.path.basename(public_path))
    assert os.path.exists(file_path)
    assert file_path.endswith(".html")


def test_generate_map_empty_input():
    with pytest.raises(ValueError):
        generate_map([])
