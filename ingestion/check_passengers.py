import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

result = connection.execute("""
SELECT COUNT(*)
FROM stg_taxi_trips
WHERE passenger_count <= 0
""").fetchone()[0]

print("Invalid passenger count trips:", result)

connection.close()