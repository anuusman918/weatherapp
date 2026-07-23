from fastapi import APIRouter
from app.services.weather_service import find_coordinates


router = APIRouter()

@router.get("/geocode")
def geocode(location: str):
    return find_coordinates(location)