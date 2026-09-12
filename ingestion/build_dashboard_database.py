import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

SOURCE_DB = BASE_DIR / "data" / "processed" / "metropulse.duckdb"
OUTPUT_DB = BASE_DIR / "data" / "processed" / "dashboard.duckdb"

source = duckdb.connect(str(SOURCE_DB), read_only=True)
output = duckdb.connect(str(OUTPUT_DB))

source_path = str(SOURCE_DB).replace("\\", "/").replace("'", "''")

output.execute(
    f"ATTACH '{source_path}' AS source (READ_ONLY)"
)

output.execute("""
CREATE OR REPLACE TABLE mart_daily_metrics AS
SELECT *
FROM source.mart_daily_metrics
""")

output.execute("""
CREATE OR REPLACE TABLE mart_hourly_metrics AS
SELECT *
FROM source.mart_hourly_metrics
""")

output.execute("""
CREATE OR REPLACE TABLE mart_payment_metrics AS
SELECT *
FROM source.mart_payment_metrics
""")

output.execute("""
CREATE OR REPLACE TABLE mart_airport_metrics AS
SELECT *
FROM source.mart_airport_metrics
""")

output.execute("""
CREATE OR REPLACE TABLE mart_quality_issues AS
SELECT *
FROM source.mart_quality_issues
""")

output.execute("""
CREATE OR REPLACE TABLE mart_weather_metrics AS
SELECT *
FROM source.mart_weather_metrics
""")

output.execute("""
CREATE OR REPLACE TABLE mart_zone_metrics AS
SELECT
    z.pickup_zone_id,
    d.zone_name,
    d.borough,
    d.service_zone,
    z.trips,
    z.passengers,
    z.total_amount,
    z.avg_distance,
    z.avg_duration,
    z.avg_fare_per_mile
FROM source.mart_zone_metrics z
LEFT JOIN source.dim_taxi_zone d
    ON z.pickup_zone_id = d.location_id
""")

output.execute("""
CREATE OR REPLACE TABLE dashboard_quality_summary AS
SELECT
    period_records,
    usable_records,
    period_records - usable_records AS excluded_records,
    CASE
        WHEN period_records > 0
        THEN (period_records - usable_records) * 100.0 / period_records
        ELSE 0
    END AS exclusion_rate_pct
FROM (
    SELECT
        (SELECT COUNT(*) FROM source.filtered_taxi_trips) AS period_records,
        (SELECT COUNT(*)
         FROM source.int_taxi_trips
         WHERE usable_for_core_metrics = 1) AS usable_records
)
""")

output.execute("""
CREATE OR REPLACE TABLE dashboard_metadata AS
SELECT
    CURRENT_TIMESTAMP AS dashboard_created_at,
    'April 1 – June 30, 2024' AS data_period,
    'NYC TLC Yellow Taxi, taxi zones, Open-Meteo historical weather' AS sources,
    'MTA Subway Hourly Ridership could not be retrieved from the required official public endpoint.' AS mta_status
""")

tables = output.execute("SHOW TABLES").fetchall()

print("Dashboard database created successfully.")
print()
print("Tables:")

for table in tables:
    print(table[0])

print()
print("Row counts:")

for table in [
    "mart_daily_metrics",
    "mart_hourly_metrics",
    "mart_zone_metrics",
    "mart_payment_metrics",
    "mart_airport_metrics",
    "mart_quality_issues",
    "mart_weather_metrics",
    "dashboard_quality_summary",
    "dashboard_metadata"
]:
    count = output.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]
    print(f"{table}: {count}")

output.execute("DETACH source")

source.close()
output.close()

print()
print(f"Created: {OUTPUT_DB}")
print(f"Size: {OUTPUT_DB.stat().st_size:,} bytes")