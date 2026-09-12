import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    COUNT(*) AS days,
    ROUND(AVG(trips), 2) AS average_daily_trips,
    MEDIAN(trips) AS median_daily_trips,
    MIN(trips) AS minimum_daily_trips,
    MAX(trips) AS maximum_daily_trips,
    ROUND(STDDEV(trips), 2) AS daily_standard_deviation,
    ROUND(
        STDDEV(trips) * 100.0 / AVG(trips),
        2
    ) AS coefficient_of_variation_percent
FROM mart_daily_metrics
"""

result = connection.execute(query).fetchdf()

print("\nDAILY DEMAND VOLATILITY")
print("-" * 45)
print(result.to_string(index=False))

connection.close()