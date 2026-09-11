import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

with open("sql/marts/core_metrics.sql", "r") as file:
    sql_code = file.read()

connection.execute(sql_code)

tables = [
    "mart_daily_metrics",
    "mart_hourly_metrics",
    "mart_zone_metrics",
    "mart_payment_metrics",
    "mart_airport_metrics",
    "mart_quality_metrics",
    "mart_day_metrics"
]

print("Marts created.")

for table in tables:
    count = connection.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]
    print(f"{table}: {count:,} rows")

connection.close()