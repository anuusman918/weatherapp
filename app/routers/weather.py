from fastapi import APIRouter, HTTPException
import requests

from app.services.weather_service import (
    find_coordinates,
    get_forecast,
    format_forecast,
)

router = APIRouter()

@router.get("/forecast")
def geocode(location: str):

    if not location.strip():
        raise HTTPException(
            status_code=400,
            detail="Location cannot be empty",
        )

    try:
        coordinates = find_coordinates(location)

        if coordinates is None:
            raise HTTPException(
                status_code=404,
                detail="Location not found",
            )

        latitude, longitude = coordinates
        data = get_forecast(latitude, longitude)

    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Weather service is currently unavailable",
        ) 

    try:
        hourly_forecast, daily_forecast = format_forecast(data)
    except (KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=502,
            detail="Invalid response received from weather service",
        )
    
    return {
    "hourly_forecast": hourly_forecast,
    "daily_forecast": daily_forecast,
    }