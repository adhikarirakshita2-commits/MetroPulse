from pathlib import Path
import requests

OUTPUT_FOLDER = Path("data/raw")
OUTPUT_FILE = OUTPUT_FOLDER / "mta_subway_hourly_ridership_2024.csv"

URL = "https://data.ny.gov/api/v3/views/wujg-7c2s/export.csv?accessType=DOWNLOAD"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

if OUTPUT_FILE.exists():
    print("MTA subway data already exists.")
else:
    print("Downloading MTA subway ridership data...")

    response = requests.get(
        URL,
        timeout=120,
        headers={
            "User-Agent": "MetroPulse Data Analysis Project"
        }
    )

    response.raise_for_status()

    OUTPUT_FILE.write_bytes(response.content)

    print("MTA subway data downloaded.")

print(f"File: {OUTPUT_FILE}")
print(f"Size: {OUTPUT_FILE.stat().st_size:,} bytes")