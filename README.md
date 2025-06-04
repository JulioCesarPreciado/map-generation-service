# map-generation-service

This microservice generates interactive maps using [Folium](https://python-visualization.github.io/folium/). It exposes a simple service that accepts a list of coordinates and returns the path to an HTML file containing the resulting map with clustered markers.

## Installation

1. Clone the repository.
2. Install the dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Import the service and call `generate_map` with a list of `(latitude, longitude)` tuples:

```python
from app.services.map_service import generate_map

markers = [
    (37.7749, -122.4194),
    (34.0522, -118.2437)
]

map_file = generate_map(markers)
print(f"Map saved to: {map_file}")
```

The function returns the path to the generated HTML file which you can open in a browser.
