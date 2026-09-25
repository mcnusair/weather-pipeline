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


# test 
# if __name__ == "__main__":
#     test_data = [
#         {'name': 'Cairo', 'main': {'temp': 304.57, 'feels_like': 303.9, 'temp_max': 304.57, 'temp_min': 300.0, 'humidity': 35}, 'wind': {'speed': 4.12}},
#         {'name': 'Lisbon', 'main': {'temp': 301.75, 'feels_like': 301.89, 'temp_max': 306.82, 'temp_min': 299.62, 'humidity': 46}, 'wind': {'speed': 4.12}},
#     ]
#     df = transform_weather(test_data)
#     print(df)