import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

checks = {
    "Invalid timestamps": """
        SELECT COUNT(*)
        FROM stg_taxi_trips
        WHERE tpep_dropoff_datetime <= tpep_pickup_datetime
    """,

    "Zero/negative distance": """
        SELECT COUNT(*)
        FROM stg_taxi_trips
        WHERE trip_distance <= 0
    """,

    "Invalid passenger count": """
        SELECT COUNT(*)
        FROM stg_taxi_trips
        WHERE passenger_count <= 0
    """,

    "Zero/negative fare": """
        SELECT COUNT(*)
        FROM stg_taxi_trips
        WHERE fare_amount <= 0
    """,

    "Negative total amount": """
        SELECT COUNT(*)
        FROM stg_taxi_trips
        WHERE total_amount < 0
    """,

    "Negative tip amount": """
        SELECT COUNT(*)
        FROM stg_taxi_trips
        WHERE tip_amount < 0
    """,

    "Very long trips": """
        SELECT COUNT(*)
        FROM stg_taxi_trips
        WHERE trip_distance > 100
    """,

    "Very high trip speed": """
        SELECT COUNT(*)
        FROM stg_taxi_trips
        WHERE trip_distance > 0
          AND EXTRACT(EPOCH FROM
              (tpep_dropoff_datetime - tpep_pickup_datetime)
          ) > 0
          AND (
              trip_distance /
              (EXTRACT(EPOCH FROM
                  (tpep_dropoff_datetime - tpep_pickup_datetime)
              ) / 3600)
          ) > 80
    """,

    "Suspicious fare vs total": """
        SELECT COUNT(*)
        FROM stg_taxi_trips
        WHERE total_amount < fare_amount
    """,

    "Invalid location IDs": """
        SELECT COUNT(*)
        FROM stg_taxi_trips
        WHERE PULocationID < 1
           OR DOLocationID < 1
    """
}

print("\nMETROPULSE DATA QUALITY CHECKS")
print("-" * 45)

for name, query in checks.items():
    result = connection.execute(query).fetchone()[0]
    print(f"{name}: {result:,}")

connection.close()