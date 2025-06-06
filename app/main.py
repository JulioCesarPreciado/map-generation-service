"""
Main entry point for the Map Generation Microservice.

This file initializes the FastAPI application, configures CORS,
serves static files, and registers the API routes.
"""

from fastapi import FastAPI
from app.api import routes
from app.config.cors import configure_cors
from app.config.static import configure_static

#: FastAPI application instance for the map generation microservice
app = FastAPI(title="Map Generation Microservice")

# Apply CORS settings to allow cross-origin requests
configure_cors(app)

# Register API routes
app.include_router(routes.router, prefix="/api")

# Serve static content like generated HTML map files
configure_static(app)
