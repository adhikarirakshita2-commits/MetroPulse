import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    precipitation_group,
    hours,
    trips,
    ROUND(avg_hourly_trips, 2) AS avg_hourly_trips,
    ROUND(avg_amount, 2) AS avg_amount,
    ROUND(avg_temperature, 2) AS avg_temperature
FROM mart_weather_metrics
ORDER BY avg_hourly_trips DESC
"""

result = connection.execute(query).fetchdf()

print("\nWEATHER AND TAXI DEMAND")
print("-" * 70)
print(result.to_string(index=False))

connection.close()