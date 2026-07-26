const searchButton = document.getElementById("search-button");
const locationInput = document.getElementById("location");
const hourlyForecastContainer = document.getElementById("hourly-forecast-container");
const currentLocationButton = document.getElementById("current-location-button")

searchButton.addEventListener("click", async () => {
    const location = locationInput.value.trim();
    let response;

    //choose the appropriate endpoint based on the user's input
    if (isCoordinates(location)) {
        const parts = location.split(",");
        const latitude = parts[0].trim();
        const longitude = parts[1].trim();

        response = await fetch(
            `/forecast/coordinates?latitude=${latitude}&longitude=${longitude}`
        );
    } else {
        response = await fetch(
            `/forecast?location=${encodeURIComponent(location)}`
        );
    }

    const data = await response.json();

    if (!response.ok) {
        alert(data.detail || "Something went wrong.");
        return;
    }

    displayForecast(data);
});

function isCoordinates(input) {
    const parts = input.split(",");

    //latitude and longitude are two parts so reject anything else
    if (parts.length !== 2) {
        return false;
    }

    const latitude = Number(parts[0].trim());
    const longitude = Number(parts[1].trim());

    //make sure its a number (since input could still be city and country so could pass previous check)
    if (Number.isNaN(latitude) || Number.isNaN(longitude)) {
        return false;
    }

    //ensure latitude and longitude are valid numbers
    return (
        latitude >= -90 &&
        latitude <= 90 &&
        longitude >= -180 &&
        longitude <= 180
    );
}

currentLocationButton.addEventListener("click", () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
});

async function success(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    const response = await fetch(
        `/forecast/coordinates?latitude=${latitude}&longitude=${longitude}`
    );

    const data = await response.json();

    if (!response.ok) {
        alert(data.detail || "Something went wrong.");
        return;
    }

    displayForecast(data);
}

function error() {
    alert("Sorry, no position is available.");
}

function displayForecast(data) {

    hourlyForecastContainer.innerHTML = "";

    //render the hourly forecast cards
    for (let i = 0; i < data.hourly_forecast.length; i++) {
        const hour = data.hourly_forecast[i];
        const hourCard = document.createElement("div");
        hourCard.classList.add("forecast-card");

        hourCard.innerHTML = `
            <p>Time: ${formatTime(hour.time)}</p>
            <p>Temperature: ${hour.temperature}°C</p>
            <p>Feels like: ${hour.apparent_temperature}°C</p>
            <p>Precipitation probability: ${hour.precipitation_probability}%</p>
            <p>Weather: ${getWeatherDescription(hour.weather_code)}</p>
        `;

        hourlyForecastContainer.appendChild(hourCard);
    }

    const dailyForecastContainer =
        document.getElementById("daily-forecast-container");

    dailyForecastContainer.innerHTML = "";
    //render the daily forecast cards
    for (let i = 0; i < data.daily_forecast.length; i++) {
        const day = data.daily_forecast[i];
        const dayCard = document.createElement("div");
        dayCard.classList.add("forecast-card");

        dayCard.innerHTML = `
            <p>Date: ${formatDate(day.date)}</p>
            <p>Maximum temperature: ${day.max_temperature}°C</p>
            <p>Mean temperature: ${day.mean_temperature}°C</p>
            <p>Minimum temperature: ${day.min_temperature}°C</p>
            <p>Weather: ${getWeatherDescription(day.weather_code)}</p>
        `;

        dailyForecastContainer.appendChild(dayCard);
    }
}
