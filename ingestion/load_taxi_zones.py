import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

with open("sql/staging/load_taxi_zones.sql", "r") as file:
    sql_code = file.read()

connection.execute(sql_code)

count = connection.execute(
    "SELECT COUNT(*) FROM dim_taxi_zone"
).fetchone()[0]

print("Taxi zone table created.")
print("Zones:", count)

connection.close()