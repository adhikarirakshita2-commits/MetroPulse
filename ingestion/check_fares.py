import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

result = connection.execute("""
SELECT COUNT(*)
FROM stg_taxi_trips
WHERE fare_amount <= 0
""").fetchone()[0]

print("Suspicious fare trips:", result)

connection.close()