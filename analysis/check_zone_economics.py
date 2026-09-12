import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    z.zone_name,
    m.trips,
    ROUND(m.trips * 100.0 / SUM(m.trips) OVER (), 2) AS trip_share_percent,
    ROUND(m.avg_distance, 2) AS avg_distance,
    ROUND(m.avg_duration, 2) AS avg_duration,
    ROUND(m.avg_fare_per_mile, 2) AS avg_fare_per_mile,
    ROUND(m.total_amount, 2) AS total_amount
FROM mart_zone_metrics m
JOIN dim_taxi_zone z
    ON m.pickup_zone_id = z.location_id
ORDER BY m.trips DESC
LIMIT 15
"""

result = connection.execute(query).fetchdf()

print("\nTOP 15 ZONES: DEMAND AND ECONOMICS")
print("-" * 90)
print(result.to_string(index=False))

connection.close()