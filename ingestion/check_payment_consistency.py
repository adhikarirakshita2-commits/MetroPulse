import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

queries = {
    "Invalid payment types": """
        SELECT COUNT(*)
        FROM int_taxi_trips
        WHERE payment_type NOT IN (1, 2, 3, 4, 5, 6)
    """,

    "Cash payments with positive tips": """
        SELECT COUNT(*)
        FROM int_taxi_trips
        WHERE payment_type = 2
          AND tip_amount > 0
    """,

    "Zero passenger count with positive distance": """
        SELECT COUNT(*)
        FROM int_taxi_trips
        WHERE passenger_count <= 0
          AND trip_distance > 0
    """,

    "Passenger count above taxi capacity": """
        SELECT COUNT(*)
        FROM int_taxi_trips
        WHERE passenger_count > 6
    """
}

print("\nMETROPULSE PAYMENT AND PASSENGER CONSISTENCY CHECKS")
print("-" * 55)

for name, query in queries.items():
    result = connection.execute(query).fetchone()[0]
    print(f"{name}: {result:,}")

connection.close()