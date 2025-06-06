import json
import os
from fastapi.testclient import TestClient
from app.main import app
from tempfile import NamedTemporaryFile
from app.services.map import generate_map
from app.schemas.markers import MapPoint

client = TestClient(app)


def create_temp_json_file(data: dict) -> NamedTemporaryFile:
    temp = NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8")
    json.dump(data, temp)
    temp.flush()
    temp.seek(0)
    return temp


def test_generate_map_from_valid_file():
    data = {
        "markers": [
            {
                "lat": 20.6736,
                "lon": -103.344,
                "label": "Centro",
                "description": "Zona Centro de Guadalajara",
                "color": "red",
                "btnUrl": "https://es.wikipedia.org/wiki/Guadalajara_(Jalisco)",
                "btnText": "Ver más"
            },
            {
                "lat": 20.6765,
                "lon": -103.347,
                "label": "Templo Expiatorio",
                "description": "Templo de estilo neogótico.",
                "color": "blue",
                "btnUrl": "https://goo.gl/maps/FzBdVj9KiwfUXYgX7",
                "btnText": "Ir al mapa"
            }
        ]
    }
    file = create_temp_json_file(data)
    headers = {"Authorization": "Bearer secreto-super-token"}
    with open(file.name, "rb") as f:
        response = client.post(
            "/api/generate-map/from-file",
            files={"file": (file.name, f, "application/json")},
            headers=headers,
        )
    assert response.status_code == 200
    assert "map_file_path" in response.json()


def test_generate_map_from_file_with_missing_fields():
    data = {
        "markers": [
            {"lat": 19.4326},
            {"lon": -103.3496},
        ]
    }
    file = create_temp_json_file(data)
    headers = {"Authorization": "Bearer secreto-super-token"}
    with open(file.name, "rb") as f:
        response = client.post(
            "/api/generate-map/from-file",
            files={"file": (file.name, f, "application/json")},
            headers=headers,
        )
    assert response.status_code == 400


def test_generate_map_from_file_with_invalid_structure():
    data = {"wrong_key": [{"lat": 19.4326, "lon": -99.1332}]}
    file = create_temp_json_file(data)
    headers = {"Authorization": "Bearer secreto-super-token"}
    with open(file.name, "rb") as f:
        response = client.post(
            "/api/generate-map/from-file",
            files={"file": (file.name, f, "application/json")},
            headers=headers,
        )
    assert response.status_code == 400


def test_generate_map_from_file_with_large_data():
    large_data = {"markers": [{"lat": float(i), "lon": float(i)} for i in range(10000)]}
    file = create_temp_json_file(large_data)
    headers = {"Authorization": "Bearer secreto-super-token"}
    with open(file.name, "rb") as f:
        response = client.post(
            "/api/generate-map/from-file",
            files={"file": (file.name, f, "application/json")},
            headers=headers,
        )
    assert response.status_code == 200
    assert "map_file_path" in response.json()


def test_generate_map_creates_file():
    markers = [
        MapPoint(lat=20.6736, lon=-103.344, label="Centro"),
        MapPoint(lat=20.6765, lon=-103.347, label="Templo Expiatorio")
    ]
    public_path = generate_map(markers)
    file_path = os.path.join("static/maps", os.path.basename(public_path))
    assert os.path.exists(file_path)
