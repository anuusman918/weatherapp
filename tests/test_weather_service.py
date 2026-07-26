from unittest.mock import patch
from app.services.weather_service import find_coordinates, get_forecast

@patch("app.services.weather_service.requests.get")
def test_find_coordinates_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "results": [
            {
                "latitude": 0,
                "longitude": 0
            }
        ]
    }

    result = find_coordinates("Manchester")

    assert result == (0, 0)
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
