from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class MapPoint(BaseModel):
    """
    Represents a single point on the map.

    Attributes:
        lat (float): Latitude coordinate.
        lon (float): Longitude coordinate.
        label (Optional[str]): A short label or title for the marker.
        description (Optional[str]): A description to be shown in the popup.
        color (Optional[str]): Optional color styling (not yet applied in rendering).
        btnUrl (Optional[str]): URL that the popup button will open.
        btnText (Optional[str]): Text for the popup button (default is "More").
    """

    lat: float
    lon: float
    label: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    btnUrl: Optional[str] = None
    btnText: Optional[str] = "More"


class MapPointList(BaseModel):
    """
    Represents a list of map points for use in API requests.

    The field 'markers' is populated using an alias for external compatibility.

    Attributes:
        markers (List[MapPoint]): A list of map point objects.
    """

    model_config = ConfigDict(populate_by_name=True)

    markers: List[MapPoint] = Field(..., alias="markers")
