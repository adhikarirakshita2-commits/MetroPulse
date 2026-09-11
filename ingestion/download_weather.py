from pathlib import Path
import requests
import pandas as pd

RAW_DATA_FOLDER = Path("data/raw")
RAW_DATA_FOLDER.mkdir(parents=True, exist_ok=True)

URL = "https://archive-api.open-meteo.com/v1/archive"

OUTPUT_FILE = RAW_DATA_FOLDER / "nyc_weather_2024-04_to_2024-06.csv"

params = {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "start_date": "2024-04-01",
    "end_date": "2024-06-30",
    "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
    "timezone": "America/New_York"
}

if OUTPUT_FILE.exists():
    print("Weather data already exists. Skipping download.")
else:
    response = requests.get(URL, params=params, timeout=60)
    response.raise_for_status()

    data = response.json()

    weather = pd.DataFrame(data["hourly"])

    weather.to_csv(OUTPUT_FILE, index=False)

    print("Weather data downloaded.")

weather = pd.read_csv(OUTPUT_FILE)

print("Rows:", len(weather))
print("Columns:", len(weather.columns))
print("Columns:", list(weather.columns))
print(weather.head().to_string(index=False))