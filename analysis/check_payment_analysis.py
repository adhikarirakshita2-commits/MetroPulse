import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    payment_type,
    trips,
    ROUND(total_amount, 2) AS total_amount,
    ROUND(avg_amount, 2) AS avg_amount,
    ROUND(avg_tip, 2) AS avg_tip,
    ROUND(avg_tip_rate, 2) AS avg_tip_rate
FROM mart_payment_metrics
ORDER BY trips DESC
"""

result = connection.execute(query).fetchdf()

print("\nPAYMENT TYPE ANALYSIS")
print("-" * 70)
print(result.to_string(index=False))

connection.close()