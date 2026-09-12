import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    airport_trip,
    trips,
    ROUND(trips * 100.0 / SUM(trips) OVER (), 2) AS trip_share_percent,
    ROUND(total_amount, 2) AS total_amount,
    ROUND(avg_amount, 2) AS avg_amount,
    ROUND(avg_distance, 2) AS avg_distance,
    ROUND(avg_duration, 2) AS avg_duration
FROM mart_airport_metrics
ORDER BY airport_trip DESC
"""

result = connection.execute(query).fetchdf()

print("\nAIRPORT TRIP ANALYSIS")
print("-" * 75)
print(result.to_string(index=False))

connection.close()