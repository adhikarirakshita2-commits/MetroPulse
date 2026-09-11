import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

result = connection.execute("""
SELECT COUNT(*)
FROM stg_taxi_trips
WHERE trip_distance <= 0
""").fetchone()[0]

print("Invalid distance trips:", result)

connection.close()