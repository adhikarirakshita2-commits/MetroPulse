import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

tests = {
    "Required period has correct row count": """
        SELECT CASE
            WHEN COUNT(*) = 10777291 THEN 0
            ELSE 1
        END
        FROM filtered_taxi_trips
    """,

    "No out-of-period records in filtered data": """
        SELECT COUNT(*)
        FROM filtered_taxi_trips
        WHERE tpep_pickup_datetime < '2024-04-01'
           OR tpep_pickup_datetime >= '2024-07-01'
    """,

    "Raw staging row count is correct": """
        SELECT CASE
            WHEN COUNT(*) = 10777315 THEN 0
            ELSE 1
        END
        FROM stg_taxi_trips
    """,

    "Source metadata contains all three months": """
        SELECT CASE
            WHEN COUNT(*) = 3 THEN 0
            ELSE 1
        END
        FROM source_metadata
    """,

    "Monthly source counts are valid": """
        SELECT COUNT(*)
        FROM source_metadata
        WHERE row_count <= 0
    """,

    "Weather has complete hourly records": """
        SELECT COUNT(*)
        FROM dim_weather
        WHERE weather_time IS NULL
    """,

    "No duplicate weather hours": """
        SELECT COUNT(*)
        FROM (
            SELECT weather_time
            FROM dim_weather
            GROUP BY weather_time
            HAVING COUNT(*) > 1
        )
    """,

    "No unmatched pickup zones": """
        SELECT COUNT(*)
        FROM int_taxi_trips t
        LEFT JOIN dim_taxi_zone z
            ON t.PULocationID = z.location_id
        WHERE t.usable_for_core_metrics = 1
          AND z.location_id IS NULL
    """,

    "No unmatched dropoff zones": """
        SELECT COUNT(*)
        FROM int_taxi_trips t
        LEFT JOIN dim_taxi_zone z
            ON t.DOLocationID = z.location_id
        WHERE t.usable_for_core_metrics = 1
          AND z.location_id IS NULL
    """,

    "Daily mart reconciles with usable trips": """
        SELECT
            (SELECT COUNT(*)
             FROM int_taxi_trips
             WHERE usable_for_core_metrics = 1)
            -
            (SELECT SUM(trips)
             FROM mart_daily_metrics)
    """
}

passed = 0

print("\nMETROPULSE AUTOMATED DATA QUALITY TESTS")
print("-" * 55)

for name, query in tests.items():
    result = connection.execute(query).fetchone()[0]

    if result == 0:
        print(f"PASS: {name}")
        passed += 1
    else:
        print(f"FAIL: {name} -> {result}")

print("-" * 55)
print(f"Tests passed: {passed}/{len(tests)}")

connection.close()