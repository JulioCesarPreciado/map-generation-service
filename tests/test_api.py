import json
from fastapi.testclient import TestClient
from app.main import app
from tempfile import NamedTemporaryFile

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
    with open(file.name, "rb") as f:
        response = client.post(
            "/api/generate-map/from-file",
            files={"file": (file.name, f, "application/json")},
        )
    assert response.status_code == 200
    assert "map_file_path" in response.json()


def test_generate_map_from_file_with_missing_fields():
    data = {
        "markers": [
            {"lat": 19.4326},  # Missing 'lon'
            {"lon": -103.3496},  # Missing 'lat'
        ]
    }
    file = create_temp_json_file(data)
    with open(file.name, "rb") as f:
        response = client.post(
            "/api/generate-map/from-file",
            files={"file": (file.name, f, "application/json")},
        )
    assert response.status_code == 400


def test_generate_map_from_file_with_invalid_structure():
    data = {"wrong_key": [{"lat": 19.4326, "lon": -99.1332}]}
    file = create_temp_json_file(data)
    with open(file.name, "rb") as f:
        response = client.post(
            "/api/generate-map/from-file",
            files={"file": (file.name, f, "application/json")},
        )
    assert response.status_code == 400


def test_generate_map_from_file_with_large_data():
    large_data = {"markers": [{"lat": float(i), "lon": float(i)} for i in range(10000)]}
    file = create_temp_json_file(large_data)
    with open(file.name, "rb") as f:
        response = client.post(
            "/api/generate-map/from-file",
            files={"file": (file.name, f, "application/json")},
        )
    assert response.status_code == 200
    assert "map_file_path" in response.json()
