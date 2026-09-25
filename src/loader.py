import pandas as pd
from pathlib import Path
from datetime import datetime
from src.logger import setup_logger


logger = setup_logger(__name__)

def save_parquet (df: pd.DataFrame, output_dir: str) -> str:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"weather_{timestamp}.parquet"
    file_path = output_path / filename
    try:
        df.to_parquet(file_path, index=False)
    except OSError as e:
        logger.exception(f"Error creating file: {e}")
    logger.info(f"Parquet file created successfully at: {file_path}")
    return str(file_path)

# test test

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    from src.extractor import WeatherAPIClient
    from src.transformer import transform_weather
    
    load_dotenv()
    base_url = os.getenv("OPENWEATHER_BASE_URL")
    cities = os.getenv("CITIES", "").split(",")
    
    client = WeatherAPIClient(base_url, cities)
    raw_data = client.get_forecast()
    df = transform_weather(raw_data)
    filepath = save_parquet(df, "data")
    print(f"Saved to: {filepath}")
