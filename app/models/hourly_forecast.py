class HourlyForecast:
    def __init__(self, time, temperature, apparent_temperature, precipitation_probability, weather_code):
        self.time = time
        self.temperature = temperature
        self.apparent_temperature = apparent_temperature
        self.precipitation_probability = precipitation_probability
        self.weather_code = weather_code

    def __repr__(self):
        return (
            f"HourlyForecast(time={self.time}, "
            f"temperature={self.temperature}, "
            f"apparent_temperature={self.apparent_temperature}, "
            f"precipitation_probability={self.precipitation_probability}, "
            f"weather_code={self.weather_code})"
        )
