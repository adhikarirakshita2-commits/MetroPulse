from pathlib import Path
import requests

RAW_DATA_FOLDER = Path("data/raw")

RAW_DATA_FOLDER.mkdir(parents=True, exist_ok=True)

TAXI_FILES = {
    "2024-04": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-04.parquet",
    "2024-05": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-05.parquet",
    "2024-06": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-06.parquet"
}

print("Taxi data download setup is ready.")
for month, url in TAXI_FILES.items():
    output_file = RAW_DATA_FOLDER / f"yellow_tripdata_{month}.parquet"

    if output_file.exists():
        print(f"{month} already exists. Skipping download.")
    else:
        print(f"Downloading {month}...")
        for attempt in range(3):
            try:
                 response = requests.get(url, timeout=60)
                 response.raise_for_status()
                 break
            except requests.RequestException as error:
                  print(f"Download attempt {attempt + 1} failed: {error}")
                  if attempt == 2:
                       raise
                  with open(output_file, "wb") as file:
                      file.write(response.content)
                      print(f"{month} downloaded.")    
import duckdb
for month in TAXI_FILES:
    file_path = RAW_DATA_FOLDER / f"yellow_tripdata_{month}.parquet"

    row_count = duckdb.read_parquet(file_path).count("*")

    print(f"{month}: {row_count} records")