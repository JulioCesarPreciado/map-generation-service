from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="Map Generation Microservice")

app.include_router(routes.router, prefix="/api")
