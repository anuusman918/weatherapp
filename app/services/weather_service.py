import requests
from app.models.hourly_forecast import HourlyForecast
from app.models.daily_forecast import DailyForecast

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


def format_forecast(data):

    #extract hourly data
    hourly_data = data["hourly"]
    time = hourly_data["time"]
    temperature_2m = hourly_data["temperature_2m"]
    apparent_temperature = hourly_data["apparent_temperature"]
    precipitation_probability = hourly_data["precipitation_probability"]
    weather_code = hourly_data["weather_code"]

    #form list of hourly data objects
    hourly_forecast = []
    # for i in range(len(time)):
    #for now return only the next twenty four hours
    for i in range(24):
        time_i = time[i]
        temperature_2m_i = temperature_2m[i]
        apparent_temperature_i = apparent_temperature[i]
        precipitation_probability_i = precipitation_probability[i]
        weather_code_i = weather_code[i]
        hourly_forecast.append(HourlyForecast(time_i, temperature_2m_i, apparent_temperature_i, precipitation_probability_i, weather_code_i))


    #extract daily data
    daily_data = data["daily"]
    date = daily_data["time"]
    temperature_2m_max = daily_data["temperature_2m_max"]
    temperature_2m_mean = daily_data["temperature_2m_mean"]
    temperature_2m_min = daily_data["temperature_2m_min"]
    weather_code_daily = daily_data["weather_code"]

    #form list of daily forecast objects
    daily_forecast = []
    for i in range(len(date)):
        date_i = date[i]
        temperature_2m_max_i = temperature_2m_max[i]
        temperature_2m_mean_i = temperature_2m_mean[i]
        temperature_2m_min_i = temperature_2m_min[i]
        weather_code_daily_i = weather_code_daily[i]
        daily_forecast.append(DailyForecast(date_i, temperature_2m_max_i, temperature_2m_mean_i, temperature_2m_min_i, weather_code_daily_i))

    return hourly_forecast, daily_forecast




# lat, long = find_coordinates("karachi")
# data = get_forecast(lat, long)
# hourly, daily = format_forecast(data)
# print(hourly)
# print(daily)







