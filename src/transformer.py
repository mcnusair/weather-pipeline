import pandas as pd
from src.logger import setup_logger

logger = setup_logger(__name__)

def transform_weather(raw_data: list[dict]) -> pd.DataFrame:
    records = []
    for city_data in raw_data:
        clean = {
            'city': city_data['name'],
            'temp_celsius': city_data['main']['temp']-273.15,
            'real_feel': city_data['main']['feels_like']-273.15,
            'temp_max' : city_data['main']['temp_max']-273.15,
            'temp_min' : city_data['main']['temp_min']-273.15,
            'humidity': city_data['main']['humidity'],
            'wind_speed': city_data['wind']['speed'],
            'fetched_at' : pd.Timestamp.now()
        }
        records.append(clean)
    logger.info("Transformed weather data for %d cities", len(records))
    return pd.DataFrame(records)
