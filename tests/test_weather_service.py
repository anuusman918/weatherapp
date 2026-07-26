from unittest.mock import patch
from app.services.weather_service import find_coordinates, get_forecast, format_forecast
import pytest

@patch("app.services.weather_service.requests.get")
def test_find_coordinates_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "results": [
            {
                "latitude": 0,
                "longitude": 0,
                "name" : "Manchester"
            }
        ]
    }

    result = find_coordinates("Manchester")

    assert result == (0, 0, "Manchester")
    mock_get.assert_called_once()


@patch("app.services.weather_service.requests.get")
def test_find_coordinates_invalid_city(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "results": []
    }
    result = find_coordinates("xyz")

    assert result is None
    mock_get.assert_called_once()

@patch("app.services.weather_service.requests.get")
def test_get_forecast_success(mock_get):
    mock_response = mock_get.return_value
    mock_result = {
        "hourly": [
            {
                "temperature": 0
            }
        ],
        "daily" : [
            {
                "temperature" : 0
            }
        ]
    }
    mock_response.json.return_value = mock_result

    result = get_forecast(0,0)

    assert result == mock_result
    mock_get.assert_called_once()


@patch("app.services.weather_service.requests.get")
def test_get_forecast_missing_daily(mock_get):
    mock_response = mock_get.return_value
    mock_result = {
        "hourly": {}
    }
    mock_response.json.return_value = mock_result

    result = get_forecast(0,0)

    assert result is None
    mock_get.assert_called_once()

@patch("app.services.weather_service.requests.get")
def test_get_forecast_missing_hourly(mock_get):
    mock_response = mock_get.return_value
    mock_result = {
        "daily": {}
    }
    mock_response.json.return_value = mock_result

    result = get_forecast(0,0)

    assert result is None
    mock_get.assert_called_once()


def test_format_forecast_success():
    data = {
        "hourly": {
            "time": [f"2026-07-26T{i:02d}:00" for i in range(24)],
            "temperature_2m": [20] * 24,
            "apparent_temperature": [19] * 24,
            "precipitation_probability": [10] * 24,
            "weather_code": [0] * 24
        },
        "daily": {
            "time": ["2026-07-26", "2026-07-27"],
            "temperature_2m_max": [25, 26],
            "temperature_2m_mean": [20, 21],
            "temperature_2m_min": [15, 16],
            "weather_code": [0, 1]
        }
    }

    hourly_forecast, daily_forecast = format_forecast(data)

    assert len(hourly_forecast) == 24
    assert len(daily_forecast) == 2

    assert hourly_forecast[0].time == "2026-07-26T00:00"
    assert hourly_forecast[0].temperature == 20
    assert hourly_forecast[0].apparent_temperature == 19
    assert hourly_forecast[0].precipitation_probability == 10
    assert hourly_forecast[0].weather_code == 0

    assert daily_forecast[0].date == "2026-07-26"
    assert daily_forecast[0].max_temperature == 25
    assert daily_forecast[0].mean_temperature == 20
    assert daily_forecast[0].min_temperature == 15
    assert daily_forecast[0].weather_code == 0




def test_format_forecast_missing_field():
    data = {
        "hourly": {},
        "daily": {}
    }

    with pytest.raises(ValueError) as exc_info:
        format_forecast(data)

    assert str(exc_info.value) == "Missing required hourly forecast field"


def test_format_forecast_insufficient_hourly_data():
    data = {
        "hourly": {
            "time": ["2026-07-26T00:00"],
            "temperature_2m": [20],
            "apparent_temperature": [19],
            "precipitation_probability": [10],
            "weather_code": [0]
        },
        "daily": {
            "time": ["2026-07-26"],
            "temperature_2m_max": [25],
            "temperature_2m_mean": [20],
            "temperature_2m_min": [15],
            "weather_code": [0]
        }
    }

    with pytest.raises(ValueError) as exc_info:
        format_forecast(data)

    assert str(exc_info.value) == \
        "Hourly forecast must contain at least 24 entries"


def test_format_forecast_mismatched_daily_lengths():
    data = {
        "hourly": {
            "time": [f"2026-07-26T{i:02d}:00" for i in range(24)],
            "temperature_2m": [20] * 24,
            "apparent_temperature": [19] * 24,
            "precipitation_probability": [10] * 24,
            "weather_code": [0] * 24
        },
        "daily": {
            "time": ["2026-07-26", "2026-07-27"],
            "temperature_2m_max": [25],
            "temperature_2m_mean": [20, 21],
            "temperature_2m_min": [15, 16],
            "weather_code": [0, 1]
        }
    }

    with pytest.raises(ValueError) as exc_info:
        format_forecast(data)

    assert str(exc_info.value) == \
        "Daily forecast fields have different lengths"