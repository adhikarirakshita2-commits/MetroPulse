import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
WITH ranked_zones AS (
    SELECT
        z.zone_name,
        m.trips,
        SUM(m.trips) OVER () AS total_trips,
        ROW_NUMBER() OVER (ORDER BY m.trips DESC) AS zone_rank
    FROM mart_zone_metrics m
    JOIN dim_taxi_zone z
        ON m.pickup_zone_id = z.location_id
)
SELECT
    zone_rank,
    zone_name,
    trips,
    ROUND(trips * 100.0 / total_trips, 2) AS trip_share_percent
FROM ranked_zones
WHERE zone_rank <= 10
ORDER BY zone_rank
"""

result = connection.execute(query).fetchdf()

print("\nTOP 10 PICKUP ZONES")
print("-" * 55)
print(result.to_string(index=False))

query_total = """
SELECT
    SUM(CASE WHEN zone_rank <= 10 THEN trips ELSE 0 END) * 100.0
    / SUM(trips) AS top_10_share_percent
FROM (
    SELECT
        trips,
        ROW_NUMBER() OVER (ORDER BY trips DESC) AS zone_rank
    FROM mart_zone_metrics
)
"""

top_10_share = connection.execute(query_total).fetchone()[0]

print("\nTOP 10 ZONE DEMAND SHARE")
print("-" * 35)
print(f"{top_10_share:.2f}%")

connection.close()