import duckdb
import pandas as pd
from src.logger import setup_logger

logger = setup_logger(__name__)

conn = duckdb.connect()

def get_temp_ranking (data_dir: str) -> pd.DataFrame:
    result1 = conn.execute(f"""
        SELECT city, temp_celsius, humidity
        FROM '{data_dir}/*.parquet'
        ORDER BY temp_celsius DESC
    """)
    df = result1.df()
    logger.info("Temperature ranking query complete — %d rows", len(df))
    return df

def get_average_temps(data_dir: str) -> pd.DataFrame:
    result2 = conn.execute(f"""
        SELECT city, ROUND(AVG(temp_celsius), 2) as avg_temp
        FROM '{data_dir}/*.parquet'
        GROUP BY city
        ORDER BY avg_temp DESC
    """)
    df = result2.df()
    logger.info("Avg temp query complete — %d rows", len(df))
    return df

def get_hottest_city_per_fetch(data_dir: str) -> pd.DataFrame:
    result3 = conn.execute(f"""
        SELECT city, temp_celsius, fetched_at,
        RANK() OVER (PARTITION BY fetched_at ORDER BY temp_celsius DESC) as temp_rank
        FROM '{data_dir}/*.parquet'
    """)
    df = result3.df()
    logger.info("Hottest city per fetch query complete — %d rows", len(df))
    return df


if __name__ == "__main__":
    print("--- Temperature Ranking ---")
    temp_ranking = get_temp_ranking("data")
    print(temp_ranking)
    
    print("--- Average Temps ---")
    avg_temps = get_average_temps("data")
    print(avg_temps)
    
    print("--- Hottest City Per Fetch ---")
    hottest = get_hottest_city_per_fetch("data")
    print(hottest)