const searchButton = document.getElementById("search-button");
const locationInput = document.getElementById("location");
const hourlyForecast = document.getElementById("hourly-forecast");
const hourlyForecastContainer = document.getElementById("hourly-forecast-container");

searchButton.addEventListener("click", async () => {
    const location = locationInput.value;

    const response = await fetch(`/forecast?location=${location}`);

    const data = await response.json();

    hourlyForecastContainer.innerHTML = "";

    for (let i = 0; i < data.hourly_forecast.length; i++) {
        const hour = data.hourly_forecast[i];

        const hourCard = document.createElement("div");

        hourCard.innerHTML = `
            <p>Time: ${formatTime(hour.time)}</p>
            <p>Temperature: ${hour.temperature}°C</p>
            <p>Feels like: ${hour.apparent_temperature}°C</p>
            <p>Precipitation probability: ${hour.precipitation_probability}%</p>
            <p>Weather code: ${getWeatherDescription(hour.weather_code)}</p>
        `;  

        hourlyForecastContainer.appendChild(hourCard);
    }

    const dailyForecastContainer =
        document.getElementById("daily-forecast-container");

    dailyForecastContainer.innerHTML = "";

    for (let i = 0; i < data.daily_forecast.length; i++) {
        const day = data.daily_forecast[i];

        const dayCard = document.createElement("div");

        dayCard.innerHTML = `
            <p>Date: ${formatDate(day.date)}</p>
            <p>Maximum temperature: ${day.max_temperature}°C</p>
            <p>Mean temperature: ${day.mean_temperature}°C</p>
            <p>Minimum temperature: ${day.min_temperature}°C</p>
            <p>Weather code: ${getWeatherDescription(day.weather_code)}</p>
        `;

        dailyForecastContainer.appendChild(dayCard);
    }
});

