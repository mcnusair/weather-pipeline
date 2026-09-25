import pytest, os
import pandas as pd
from unittest.mock import patch
from src.extractor import WeatherAPIClient

def test_get_forecast():
    """Assuring get_forecast() returns data, a list of dictionaries"""
    fake_response = {'name': 'Cairo', 'main': {'temp': 304.57, 'feels_like': 303.9, 'temp_max': 304.57, 'temp_min': 300.0, 'humidity': 35}, 'wind': {'speed': 4.12}}
    with patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test_key"}):
        with patch("src.extractor.requests.Session") as mock_session:
            mock_session.return_value.get.return_value.json.return_value = fake_response
            mock_session.return_value.get.return_value.raise_for_status = lambda:None
            client = WeatherAPIClient("https://fake-url.com", ["Cairo"])
            result = client.get_forecast()
            assert result == [fake_response]

def test_missing_api_key_raises_value_error():
    """Tests that WeatherAPIClient raises a ValueError when the API key is not set"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            WeatherAPIClient("https://fake-url.com", ["Cairo"])


