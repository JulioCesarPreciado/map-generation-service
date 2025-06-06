from fastapi import FastAPI
from app.api import routes
from app.config.cors import configure_cors
from app.config.static import configure_static

app = FastAPI(title="Map Generation Microservice")

configure_cors(app)

app.include_router(routes.router, prefix="/api")

configure_static(app)
