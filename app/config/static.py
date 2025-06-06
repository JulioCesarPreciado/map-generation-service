from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os


def configure_static(app: FastAPI):
    """
    Configures the static file mounting in the FastAPI application.

    This implementation serves files from the local 'static' directory,
    accessible via the '/static' route.

    For production, this function can be modified to serve files from
    storage services like MinIO or Amazon S3, using custom middleware
    or URL redirection through a CDN or reverse proxy.
    """
    static_path = "static"
    if os.path.exists(static_path):
        app.mount("/static", StaticFiles(directory=static_path), name="static")
