from fastapi import FastAPI
from src.routers import city_router, earthquake_router
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(city_router.router)
app.include_router(earthquake_router.router)
