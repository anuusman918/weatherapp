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
            <p>Time: ${hour.time}</p>
            <p>Temperature: ${hour.temperature}°C</p>
            <p>Feels like: ${hour.apparent_temperature}°C</p>
            <p>Precipitation probability: ${hour.precipitation_probability}%</p>
            <p>Weather code: ${hour.weather_code}</p>
        `;

        hourlyForecastContainer.appendChild(hourCard);
    }

    console.log(data);
});

