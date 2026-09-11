import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

raw_count = connection.execute("""
    SELECT COUNT(*)
    FROM stg_taxi_trips
""").fetchone()[0]

period_count = connection.execute("""
    SELECT COUNT(*)
    FROM filtered_taxi_trips
""").fetchone()[0]

usable_count = connection.execute("""
    SELECT COUNT(*)
    FROM int_taxi_trips
    WHERE usable_for_core_metrics = 1
""").fetchone()[0]

daily_count = connection.execute("""
    SELECT SUM(trips)
    FROM mart_daily_metrics
""").fetchone()[0]

print("Raw staging records:", raw_count)
print("Records in required period:", period_count)
print("Usable records:", usable_count)
print("Records in daily mart:", daily_count)

connection.close()