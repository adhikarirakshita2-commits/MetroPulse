import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT COUNT(*)
FROM int_taxi_trips t
LEFT JOIN dim_taxi_zone z
    ON t.PULocationID = z.location_id
WHERE t.usable_for_core_metrics = 1
  AND z.location_id IS NULL
"""

result = connection.execute(query).fetchone()[0]

print("Trips with unmatched pickup zones:", result)

connection.close()