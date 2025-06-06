from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.security import HTTPBearer
from app.services.map import generate_map
from app.schemas.markers import MapPointList
from app.dependencies.auth import get_current_user

router = APIRouter()
security = HTTPBearer()


@router.post("/generate-map", summary="Generar un mapa con marcadores")
def create_map(data: MapPointList, user=Depends(get_current_user)):
    try:
        path = generate_map(data.markers)
        return {"map_file_path": path}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate-map/from-file", summary="Generar mapa desde archivo JSON")
async def create_map_from_file(
    file: UploadFile = File(...), user=Depends(get_current_user)
):
    try:
        contents = await file.read()
        parsed = MapPointList.model_validate_json(contents)
        path = generate_map(parsed.markers)
        return {"map_file_path": path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
