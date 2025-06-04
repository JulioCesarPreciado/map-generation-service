from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
from app.services.map_service import generate_map

app = FastAPI(title="Map Generation Microservice")


class MarkerList(BaseModel):
    markers: List[Tuple[float, float]]


@app.post("/generate-map/")
def create_map(marker_list: MarkerList):
    try:
        path = generate_map(marker_list.markers)
        return {"map_file_path": path}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
