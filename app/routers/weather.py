from fastapi import APIRouter, HTTPException, Request
import requests
from fastapi.templating import Jinja2Templates

from app.services.weather_service import (
    find_coordinates,
    get_forecast,
    format_forecast,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@router.get("/forecast")
def forecast(location: str):

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

        latitude, longitude, location_name = coordinates
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
        "location": location_name,
        "hourly_forecast": hourly_forecast,
        "daily_forecast": daily_forecast,
    }



@router.get("/forecast/coordinates")
def forecast_by_coordinates(latitude: float, longitude: float):
    try:
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
        "location": f"{latitude:.4f}, {longitude:.4f}",
        "hourly_forecast": hourly_forecast,
        "daily_forecast": daily_forecast,
    }