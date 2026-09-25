import os
from dotenv import load_dotenv
from src.logger import setup_logger
from src.extractor import WeatherAPIClient
from src.transformer import transform_weather
from src.loader import save_parquet
from src.analysis import get_temp_ranking, get_average_temps, get_hottest_city_per_fetch

logger = setup_logger(__name__)

def run():
    logger.info("Pipeline started")
    try:
        load_dotenv()
        base_url = os.getenv("OPENWEATHER_BASE_URL")
        cities = [city.strip() for city in os.getenv("CITIES", "").split(",") if city.strip()]
        data_dir = os.getenv("DATA_DIR", "data")

        # extract
        client = WeatherAPIClient(base_url, cities)
        raw_data = client.get_forecast()

        # transform
        df = transform_weather(raw_data)

        # load
        filepath = save_parquet(df, data_dir)

        # analysis
        temp_ranking = get_temp_ranking(data_dir)
        logger.info("Temperature ranking generated with %d rows", len(temp_ranking))
        avg_temp = get_average_temps(data_dir)
        logger.info("Average temp generated with %d rows", len(avg_temp))
        hottest_city_per_fetch = get_hottest_city_per_fetch(data_dir)
        logger.info("Hottest city per fetch generated with %d rows", len(hottest_city_per_fetch))


    except Exception as e:
        logger.exception("Pipeline failed: %s", e)
        raise
    finally:
        logger.info("Pipeline finished")

if __name__ == "__main__":
    run()


