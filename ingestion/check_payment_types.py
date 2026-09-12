import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    payment_type,
    COUNT(*) AS trips
FROM int_taxi_trips
GROUP BY payment_type
ORDER BY payment_type
"""

result = connection.execute(query).fetchdf()

print("\nPAYMENT TYPE DISTRIBUTION")
print("-" * 35)
print(result.to_string(index=False))

connection.close()