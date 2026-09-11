import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

duplicate_hours = connection.execute("""
    SELECT COUNT(*)
    FROM (
        SELECT weather_time
        FROM dim_weather
        GROUP BY weather_time
        HAVING COUNT(*) > 1
    )
""").fetchone()[0]

missing_weather = connection.execute("""
    SELECT COUNT(*)
    FROM int_weather_analysis
    WHERE temperature IS NULL
""").fetchone()[0]

print("Duplicate weather hours:", duplicate_hours)
print("Hours with missing weather:", missing_weather)

connection.close()