import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    payment_type,
    trips,
    ROUND(avg_tip, 2) AS avg_tip,
    ROUND(avg_tip_rate, 2) AS avg_tip_rate
FROM mart_payment_metrics
WHERE payment_type IN (1, 2, 3, 4)
ORDER BY payment_type
"""

result = connection.execute(query).fetchdf()

print("\nTIPPING BY CLASSIFIED PAYMENT TYPE")
print("-" * 60)
print(result.to_string(index=False))

query_total = """
SELECT
    COUNT(*) AS trips_with_positive_tip
FROM int_taxi_trips
WHERE usable_for_core_metrics = 1
  AND tip_amount > 0
"""

positive_tips = connection.execute(query_total).fetchone()[0]

print("\nTRIPS WITH POSITIVE TIPS")
print("-" * 35)
print(f"{positive_tips:,}")

connection.close()