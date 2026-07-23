from fastapi import APIRouter
from app.services.weather_service import (
    find_coordinates,
    get_forecast,
    format_forecast,
)

router = APIRouter()

@router.get("/forecast")
def geocode(location: str):
    latitude, longitude = find_coordinates(location)
    data = get_forecast(latitude, longitude)
    hourly_forecast, daily_forecast = format_forecast(data)
    return hourly_forecast, daily_forecast