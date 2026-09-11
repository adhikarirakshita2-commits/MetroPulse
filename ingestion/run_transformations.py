import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

# Read the SQL transformation file
with open("sql/intermediate/taxi_transformations.sql", "r") as file:
    sql_code = file.read()

# Run all transformations
connection.execute(sql_code)

# Check final table
row_count = connection.execute(
    "SELECT COUNT(*) FROM int_taxi_trips"
).fetchone()[0]

column_count = connection.execute(
    "SELECT COUNT(*) "
    "FROM information_schema.columns "
    "WHERE table_name = 'int_taxi_trips'"
).fetchone()[0]

print("Transformations completed.")
print("Final rows:", row_count)
print("Final columns:", column_count)

connection.close()