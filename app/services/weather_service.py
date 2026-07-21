import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

#receives location from user and gets latitude and longitude
def find_coordinates(location):
    #get data for the city searched for - takes first result
    response = requests.get(GEOCODING_URL, params={
    "name": location,
    "count": 1
    })
    response.raise_for_status() 
    data = response.json()

    #make sure a valid city is returned
    if "results" not in data or not data["results"]:
        print("No matching city was found")
        return None
    
    first_result = data["results"][0]
    latitude = first_result["latitude"]
    longitude = first_result["longitude"]
    return latitude, longitude


FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

#receives latitude and longitude and gets weather data
def get_forecast(latitude, longitude):
    params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": "temperature_2m,apparent_temperature,precipitation_probability,weather_code",
    "daily": "temperature_2m_max,temperature_2m_mean,temperature_2m_min,weather_code",
    "timezone": "auto"
    }
    response = requests.get(FORECAST_URL, params=params)
    response.raise_for_status() 
    data = response.json()

    #ensure weather data is returned
    if "hourly" not in data or "daily" not in data:
        print("No weather data was found")
        return None
    
    return data



