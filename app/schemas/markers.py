from pydantic import BaseModel
from typing import List, Tuple


class MarkerList(BaseModel):
    markers: List[Tuple[float, float]]
