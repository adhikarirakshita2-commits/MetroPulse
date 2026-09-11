from pathlib import Path
import requests
import pandas as pd
import zipfile

RAW_DATA_FOLDER = Path("data/raw")
RAW_DATA_FOLDER.mkdir(parents=True, exist_ok=True)

LOOKUP_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
SHAPEFILE_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip"

LOOKUP_FILE = RAW_DATA_FOLDER / "taxi_zone_lookup.csv"
ZIP_FILE = RAW_DATA_FOLDER / "taxi_zones.zip"
SHAPEFILE_FOLDER = RAW_DATA_FOLDER / "taxi_zones"

if LOOKUP_FILE.exists():
    print("Taxi zone lookup already exists. Skipping download.")
else:
    response = requests.get(LOOKUP_URL, timeout=60)
    response.raise_for_status()

    with open(LOOKUP_FILE, "wb") as file:
        file.write(response.content)

    print("Taxi zone lookup downloaded.")

if ZIP_FILE.exists():
    print("Taxi zone shapefile already exists. Skipping download.")
else:
    response = requests.get(SHAPEFILE_URL, timeout=60)
    response.raise_for_status()

    with open(ZIP_FILE, "wb") as file:
        file.write(response.content)

    print("Taxi zone shapefile downloaded.")

SHAPEFILE_FOLDER.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(ZIP_FILE, "r") as zip_file:
    zip_file.extractall(SHAPEFILE_FOLDER)

print("Taxi zone shapefile extracted.")

data = pd.read_csv(LOOKUP_FILE)

print("Lookup rows:", len(data))
print("Lookup columns:", len(data.columns))
print("Shapefile files:", len(list(SHAPEFILE_FOLDER.iterdir())))