import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

with open("sql/intermediate/destination_zone_analysis.sql", "r") as file:
    sql_code = file.read()

connection.execute(sql_code)

count = connection.execute(
    "SELECT COUNT(*) FROM int_destination_zone_analysis"
).fetchone()[0]

print("Destination zone analysis table created.")
print("Zones:", count)

result = connection.execute("""
    SELECT
        zone_name,
        borough,
        trips,
        total_amount
    FROM int_destination_zone_analysis
    ORDER BY trips DESC
    LIMIT 10
""").fetchdf()

print(result.to_string(index=False))

connection.close()