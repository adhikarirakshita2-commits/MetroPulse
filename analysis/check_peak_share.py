import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    demand_period,
    SUM(trips) AS trips,
    ROUND(
        SUM(trips) * 100.0 /
        (SELECT SUM(trips) FROM mart_hourly_metrics),
        2
    ) AS trip_share_percent
FROM mart_hourly_metrics
GROUP BY demand_period
ORDER BY trips DESC
"""

result = connection.execute(query).fetchdf()

print("\nPEAK VS OFF-PEAK DEMAND")
print("-" * 40)
print(result.to_string(index=False))

connection.close()