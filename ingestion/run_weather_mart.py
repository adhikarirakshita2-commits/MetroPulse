import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

with open("sql/marts/weather_metrics.sql", "r") as file:
    sql_code = file.read()

connection.execute(sql_code)

result = connection.execute("""
    SELECT *
    FROM mart_weather_metrics
    ORDER BY avg_hourly_trips DESC
""").fetchdf()

print("Weather mart created.")
print(result.to_string(index=False))

connection.close()