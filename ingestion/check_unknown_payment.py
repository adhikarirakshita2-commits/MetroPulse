import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    payment_type,
    COUNT(*) AS trips,
    SUM(fare_amount) AS total_fare,
    SUM(tip_amount) AS total_tip,
    SUM(total_amount) AS total_amount,
    AVG(fare_amount) AS avg_fare,
    AVG(tip_amount) AS avg_tip
FROM int_taxi_trips
WHERE payment_type IN (0, 5)
GROUP BY payment_type
ORDER BY payment_type
"""

result = connection.execute(query).fetchdf()

print("\nUNKNOWN AND UNUSUAL PAYMENT TYPES")
print("-" * 50)
print(result.to_string(index=False))

connection.close()
