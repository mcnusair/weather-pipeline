import requests, os
from src.logger import setup_logger
from dotenv import load_dotenv

logger = setup_logger(__name__)

class WeatherAPIClient:

    def __init__(self, base_url, cities):
        self.base_url = base_url
        self.cities = cities
        self.session = requests.Session()
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY is not set")
        

    def get_forecast(self) -> list[dict]:
        results = []
        for city in self.cities:
            try:
                response = self.session.get(self.base_url, params={"appid": self.api_key, "q": city})
                response.raise_for_status()
                results.append(response.json())
                logger.info("Fetched weather for %s", city)
            except requests.exceptions.HTTPError as e:
                logger.exception(f" HTTP error: {e}")
                raise
            except requests.exceptions.RequestException as e:
                logger.exception(f"Request error: {e}")
                raise
        return results  

# Quick testing

# load_dotenv()
# base_url = os.getenv("OPENWEATHER_BASE_URL")
# cities = [city.strip() for city in os.getenv("CITIES", "").split(",") if city.strip()]
# client = WeatherAPIClient(base_url,cities)
# results = client.get_forecast()
# print (results)


