# Weather Pipeline
 
A Python data pipeline that fetches live weather data for multiple cities, transforms it, stores it as Parquet files, and runs SQL analytics on it using DuckDB. Structured logging, exception handling, environment-based config, and a full test suite.
 
---
 
## What it does
 
Every run calls the OpenWeather API for a configurable list of cities, converts the raw JSON into a clean pandas DataFrame with temperatures in Celsius and a fetch timestamp added, and writes the result to a timestamped Parquet file in a local data/ folder. Three DuckDB queries then run against the stored files: current temperature ranking across cities, average temperature per city across all runs, and a per-fetch hottest city ranking using a window function. All credentials come from .env, all steps are logged with named loggers, and all external calls have exception handling.
 
---
 
## Architecture
 
```
OpenWeather API
      |
      v
extractor.py  (WeatherAPIClient)
      |  list of raw dicts per city
      v
transformer.py  (transform_weather)
      |  clean pandas DataFrame, Kelvin to Celsius, timestamp added
      v
loader.py  (save_parquet)
      |  data/weather_YYYYMMDD_HHMMSS.parquet
      v
analysis.py  (DuckDB queries)
      |  temperature ranking, city averages, hottest city per fetch
      v
pipeline.py  (orchestrates all steps in sequence)
```
 
---
 
## Setup
 
**1. Clone the repo**
 
```bash
git clone https://github.com/mcnusair/weather-pipeline.git
cd weather-pipeline
```
 
**2. Create and activate a virtual environment**
 
```bash
python3 -m venv .venv
source .venv/bin/activate
```
 
**3. Install dependencies**
 
```bash
pip install -r requirements.txt
```
 
**4. Create a .env file in the project root**
 
```
OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5/weather
CITIES=Cairo,Lisbon,Valencia
DATA_DIR=data
LOG_LEVEL=INFO
```
 
Free API keys at openweathermap.org. New keys take up to 2 hours to activate.
 
---
 
## How to run
 
```bash
python -m src.pipeline
```
 
To see debug output:
 
```bash
LOG_LEVEL=DEBUG python -m src.pipeline
```
 
---
 
## Schedule with cron
 
To run the pipeline automatically every day at 8am, open your crontab:
 
```bash
crontab -e
```
 
Add this line, updating the paths to match your setup:
 
```
0 8 * * * cd /path/to/weather-pipeline && LOG_LEVEL=INFO /path/to/.venv/bin/python -m src.pipeline >> /path/to/weather-pipeline/pipeline.log 2>&1
```
 
The pipeline output and any errors are appended to pipeline.log on every run.
 
---
 
## Run tests
 
```bash
pytest -v
```
 
---
 
## Project structure
 
```
weather-pipeline/
    src/
        __init__.py         marks src as a Python package
        logger.py           shared logger setup, imported by all modules
        extractor.py        WeatherAPIClient class, fetches from OpenWeather API
        transformer.py      cleans raw response, converts Kelvin to Celsius, adds timestamp
        loader.py           saves DataFrame to a timestamped Parquet file
        analysis.py         three DuckDB queries on the stored Parquet files
        pipeline.py         orchestrates all steps in sequence
    tests/
        test_extractor.py   tests for WeatherAPIClient with mocked API calls
        test_transformer.py tests for transform_weather, happy path and empty input
    data/                   Parquet output files, git-ignored
    .env                    credentials and config, never committed
    .gitignore              excludes .env, .venv, data/, __pycache__
    conftest.py             tells pytest to use the project root for imports
    requirements.txt        locked dependency versions
    README.md               this file
```
 
---
 
## Output schema
 
One row per city per run:
 
| Column | Type | Description |
|--------|------|-------------|
| city | string | City name |
| temp_celsius | float | Current temperature in Celsius |
| real_feel | float | Feels-like temperature in Celsius |
| temp_max | float | Max temperature in Celsius |
| temp_min | float | Min temperature in Celsius |
| humidity | int | Humidity percentage |
| wind_speed | float | Wind speed in metres per second |
| fetched_at | timestamp | When this row was fetched |
 
---
 
## Stack
 
| Tool | What it does |
|------|-------------|
| Python 3.14 | Pipeline language |
| requests | HTTP calls to the OpenWeather API |
| pandas | Transformation and Parquet I/O |
| pyarrow | Parquet engine used by pandas |
| DuckDB | SQL analytics on local Parquet files |
| python-dotenv | Loads credentials from .env |
| pytest | Unit tests with mocked API calls |
 # tested credential manager
