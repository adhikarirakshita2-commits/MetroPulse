from pathlib import Path
import duckdb

DATABASE_FOLDER = Path("data/processed")
DATABASE_FOLDER.mkdir(parents=True, exist_ok=True)

DATABASE_FILE = DATABASE_FOLDER / "metropulse.duckdb"

connection = duckdb.connect(str(DATABASE_FILE))

print("MetroPulse database connected.")

connection.execute("""
CREATE OR REPLACE TABLE stg_taxi_trips AS
SELECT *
FROM read_parquet('data/raw/yellow_tripdata_2024-04.parquet')

UNION ALL

SELECT *
FROM read_parquet('data/raw/yellow_tripdata_2024-05.parquet')

UNION ALL

SELECT *
FROM read_parquet('data/raw/yellow_tripdata_2024-06.parquet');
""")

row_count = connection.execute(
    "SELECT COUNT(*) FROM stg_taxi_trips"
).fetchone()[0]
column_count = connection.execute("""
SELECT COUNT(*)
FROM information_schema.columns
WHERE table_name = 'stg_taxi_trips'
""").fetchone()[0]

print("stg_taxi_trips created.")
print("Total records:", row_count)
print("Total columns:", column_count)
connection.close()