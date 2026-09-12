import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

with open("sql/marts/core_metrics.sql", "r") as file:
    core_sql = file.read()

connection.execute(core_sql)

with open("sql/marts/quality_metrics.sql", "r") as file:
    quality_sql = file.read()

connection.execute(quality_sql)

tables = [
    "mart_daily_metrics",
    "mart_hourly_metrics",
    "mart_zone_metrics",
    "mart_payment_metrics",
    "mart_airport_metrics",
    "mart_quality_metrics",
    "mart_quality_issues",
    "mart_day_metrics"
]

print("Marts created.")

for table in tables:
    count = connection.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]
    print(f"{table}: {count:,} rows")

connection.close()