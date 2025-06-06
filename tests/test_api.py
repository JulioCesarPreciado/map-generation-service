import json
import os
from fastapi.testclient import TestClient
from app.main import app
from tempfile import NamedTemporaryFile
from app.services.map import generate_map

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
            {"lat": 19.4326, "lon": -99.1332},
            {"lat": 20.6597, "lon": -103.3496},
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
    markers = [(19.4326, -99.1332), (20.6597, -103.3496)]
    public_path = generate_map(markers)
    file_path = os.path.join("static/maps", os.path.basename(public_path))
    assert os.path.exists(file_path)
