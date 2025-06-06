from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def configure_static(app: FastAPI):
    """
    Configures the static file mounting in the FastAPI application.

    This implementation serves files from the local 'static' directory,
    accessible via the '/static' route.

    For production, this function can be modified to serve files from
    storage services like MinIO or Amazon S3, using custom middleware
    or URL redirection through a CDN or reverse proxy.
    """
    app.mount("/static", StaticFiles(directory="static"), name="static")
