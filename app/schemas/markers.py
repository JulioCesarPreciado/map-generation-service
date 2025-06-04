from pydantic import BaseModel, Field
from typing import List, Optional


class MapPoint(BaseModel):
    lat: float
    lon: float
    label: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None


class MapPointList(BaseModel):
    markers: List[MapPoint] = Field(..., alias="markers")
