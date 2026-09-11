from pathlib import Path
import requests

RAW_DATA_FOLDER = Path("data/raw")
RAW_DATA_FOLDER.mkdir(parents=True, exist_ok=True)

URL = "https://data.ny.gov/api/views/wujg-7c2s/rows.csv?accessType=DOWNLOAD"

OUTPUT_FILE = RAW_DATA_FOLDER / "mta_subway_hourly_2024.csv"

if OUTPUT_FILE.exists():
    print("Subway data already exists. Skipping download.")
else:
    response = requests.get(URL, timeout=120)
    response.raise_for_status()

    with open(OUTPUT_FILE, "wb") as file:
        file.write(response.content)

    print("Subway data downloaded.")

print("File:", OUTPUT_FILE)
print("Size:", OUTPUT_FILE.stat().st_size, "bytes")