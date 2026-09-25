from src.transformer import transform_weather
import pytest 
import pandas as pd

@pytest.fixture
def sample_data():
    """Provides valid raw OpenWeather API payload for testing."""
    return [
       {'name': 'Cairo', 'main': {'temp': 304.57, 'feels_like': 303.9, 'temp_max': 304.57, 'temp_min': 300.0, 'humidity': 35}, 'wind': {'speed': 4.12}},
        {'name': 'Lisbon', 'main': {'temp': 301.75, 'feels_like': 301.89, 'temp_max': 306.82, 'temp_min': 299.62, 'humidity': 46}, 'wind': {'speed': 4.12}},
   ]

def test_transform_weather_happy_path(sample_data):
    """Tests successful transformation into a pandas dataframe"""
    df = transform_weather(sample_data)
    # Assert structure
    assert isinstance(df, pd.DataFrame)
    assert len(df) ==2
    assert list(df.columns) == ['city','temp_celsius', 'real_feel', 'temp_max', 'temp_min', 'humidity', 'wind_speed', 'fetched_at']
    # assert correct values
    row = df.iloc[0]
    assert row['city'] == 'Cairo'
    assert pytest.approx(row['temp_celsius'], 0.01) == 31.42
    assert pytest.approx(row['real_feel'], 0.01) == 30.75
    assert pytest.approx(row['temp_max'], 0.01) == 31.42
    assert pytest.approx(row['temp_min'], 0.01) == 26.85
    assert row['humidity'] == 35
    assert row['wind_speed'] == 4.12

def test_transform_weather_empty_list():
    """ Tests behaviour when passing empty list"""
    df = transform_weather([])
    assert isinstance(df, pd.DataFrame)
    assert df.empty
