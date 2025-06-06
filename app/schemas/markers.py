from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class MapPoint(BaseModel):
    lat: float
    lon: float
    label: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    btnUrl: Optional[str] = None
    btnText: Optional[str] = "More"


class MapPointList(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    markers: List[MapPoint] = Field(..., alias="markers")
