import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    pickup_day,
    trips,
    total_amount,
    avg_amount,
    avg_duration,
    avg_distance
FROM mart_day_metrics
ORDER BY trips DESC
"""

result = connection.execute(query).fetchdf()

print("\nTAXI DEMAND BY DAY OF WEEK")
print("-" * 45)
print(result.to_string(index=False))

connection.close()