class DailyForecast:
    def __init__(self, date, max_temperature, mean_temperature, min_temperature, weather_code):
        self.date = date
        self.max_temperature = max_temperature
        self.mean_temperature = mean_temperature
        self.min_temperature = min_temperature
        self.weather_code = weather_code

    def __repr__(self):
        return (
            f"DailyForecast(time={self.date}, "
            f"max_temperature={self.max_temperature}, "
            f"mean_temperature={self.mean_temperature}, "
            f"min_temperature={self.min_temperature}, "
            f"weather_code={self.weather_code})"
        )