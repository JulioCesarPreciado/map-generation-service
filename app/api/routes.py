from fastapi import APIRouter, HTTPException
from app.services.map import generate_map
from app.schemas.markers import MarkerList

router = APIRouter()


@router.post("/generate-map", summary="Generar un mapa con marcadores")
def create_map(marker_list: MarkerList):
    try:
        path = generate_map(marker_list.markers)
        return {"map_file_path": path}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
