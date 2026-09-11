import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

connection.execute("""
CREATE OR REPLACE TABLE dim_weather AS
SELECT
    CAST(time AS TIMESTAMP) AS weather_time,
    temperature_2m,
    relative_humidity_2m,
    precipitation,
    wind_speed_10m,
    weather_code
FROM read_csv_auto('data/raw/nyc_weather_2024-04_to_2024-06.csv');
""")

count = connection.execute(
    "SELECT COUNT(*) FROM dim_weather"
).fetchone()[0]

print("Weather table created.")
print("Weather records:", count)

connection.close()