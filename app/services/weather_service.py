import requests
from app.models.hourly_forecast import HourlyForecast
from app.models.daily_forecast import DailyForecast

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

#gets latitude and longitude for first matching result for a city/country
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

#gets weather data from Meteo
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

#validates weather data and formats data into HourlyForecast and DailyForecast object lists
def format_forecast(data):
    if not isinstance(data, dict):
        raise ValueError("Forecast data must be a dictionary")

    if "hourly" not in data or "daily" not in data:
        raise ValueError("Missing hourly or daily forecast data")

    hourly_data = data["hourly"]
    daily_data = data["daily"]

    required_hourly_fields = [
        "time",
        "temperature_2m",
        "apparent_temperature",
        "precipitation_probability",
        "weather_code"
    ]

    required_daily_fields = [
        "time",
        "temperature_2m_max",
        "temperature_2m_mean",
        "temperature_2m_min",
        "weather_code"
    ]

    if any(field not in hourly_data for field in required_hourly_fields):
        raise ValueError("Missing required hourly forecast field")

    if any(field not in daily_data for field in required_daily_fields):
        raise ValueError("Missing required daily forecast field")

    if any(len(hourly_data[field]) < 24 for field in required_hourly_fields):
        raise ValueError("Hourly forecast must contain at least 24 entries")

    daily_length = len(daily_data["time"])

    if any(
        len(daily_data[field]) != daily_length
        for field in required_daily_fields
    ):
        raise ValueError("Daily forecast fields have different lengths")

    hourly_data = data["hourly"]
    time = hourly_data["time"]
    temperature_2m = hourly_data["temperature_2m"]
    apparent_temperature = hourly_data["apparent_temperature"]
    precipitation_probability = hourly_data["precipitation_probability"]
    weather_code = hourly_data["weather_code"]


    hourly_forecast = []
    #return only the next 24 hours to keep the forecast concise
    for i in range(24):
        time_i = time[i]
        temperature_2m_i = temperature_2m[i]
        apparent_temperature_i = apparent_temperature[i]
        precipitation_probability_i = precipitation_probability[i]
        weather_code_i = weather_code[i]
        hourly_forecast.append(HourlyForecast(time_i, temperature_2m_i, apparent_temperature_i, precipitation_probability_i, weather_code_i))


    daily_data = data["daily"]
    date = daily_data["time"]
    temperature_2m_max = daily_data["temperature_2m_max"]
    temperature_2m_mean = daily_data["temperature_2m_mean"]
    temperature_2m_min = daily_data["temperature_2m_min"]
    weather_code_daily = daily_data["weather_code"]


    daily_forecast = []
    for i in range(len(date)):
        date_i = date[i]
        temperature_2m_max_i = temperature_2m_max[i]
        temperature_2m_mean_i = temperature_2m_mean[i]
        temperature_2m_min_i = temperature_2m_min[i]
        weather_code_daily_i = weather_code_daily[i]
        daily_forecast.append(DailyForecast(date_i, temperature_2m_max_i, temperature_2m_mean_i, temperature_2m_min_i, weather_code_daily_i))

    return hourly_forecast, daily_forecast










