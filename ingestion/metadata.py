from pathlib import Path
from datetime import datetime
import hashlib
import duckdb

RAW_DATA_FOLDER = Path("data/raw")
DATABASE_FILE = "data/processed/metropulse.duckdb"

TAXI_FILES = {
    "2024-04": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-04.parquet",
    "2024-05": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-05.parquet",
    "2024-06": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-06.parquet"
}

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(1024 * 1024)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()

connection = duckdb.connect(DATABASE_FILE)

connection.execute("""
CREATE OR REPLACE TABLE source_metadata (
    source_name VARCHAR,
    source_url VARCHAR,
    period VARCHAR,
    extraction_timestamp TIMESTAMP,
    row_count BIGINT,
    file_name VARCHAR,
    file_size_bytes BIGINT,
    sha256 VARCHAR
)
""")

extraction_time = datetime.now()

for period, url in TAXI_FILES.items():
    file_path = RAW_DATA_FOLDER / f"yellow_tripdata_{period}.parquet"

    row_count = connection.execute(
        f"SELECT COUNT(*) FROM read_parquet('{file_path}')"
    ).fetchone()[0]

    file_size = file_path.stat().st_size
    file_hash = calculate_hash(file_path)

    connection.execute(
        """
        INSERT INTO source_metadata
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            "NYC TLC Yellow Taxi Trip Records",
            url,
            period,
            extraction_time,
            row_count,
            file_path.name,
            file_size,
            file_hash
        ]
    )

connection.close()

print("Source metadata saved.")