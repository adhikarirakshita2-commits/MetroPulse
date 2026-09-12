import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT COUNT(*)
FROM (
    SELECT
        VendorID,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        PULocationID,
        DOLocationID,
        fare_amount,
        total_amount,
        COUNT(*) AS duplicate_count
    FROM int_taxi_trips
    GROUP BY
        VendorID,
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        passenger_count,
        trip_distance,
        PULocationID,
        DOLocationID,
        fare_amount,
        total_amount
    HAVING COUNT(*) > 1
)
"""

result = connection.execute(query).fetchone()[0]

print("Duplicate record groups:", result)

connection.close()