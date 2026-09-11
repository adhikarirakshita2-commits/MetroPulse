import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

with open("sql/intermediate/weather_analysis.sql", "r") as file:
    sql_code = file.read()

connection.execute(sql_code)

count = connection.execute(
    "SELECT COUNT(*) FROM int_weather_analysis"
).fetchone()[0]

matched = connection.execute("""
    SELECT COUNT(*)
    FROM int_weather_analysis
    WHERE temperature IS NOT NULL
""").fetchone()[0]

print("Weather analysis table created.")
print("Hourly records:", count)
print("Hours with weather data:", matched)

connection.close()