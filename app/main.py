from fastapi import FastAPI
from app.routers.weather import router

app = FastAPI()
app.include_router(router)