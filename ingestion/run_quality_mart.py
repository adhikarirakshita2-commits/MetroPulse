import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

with open("sql/marts/quality_metrics.sql", "r") as file:
    sql_code = file.read()

connection.execute(sql_code)

result = connection.execute("""
    SELECT *
    FROM mart_quality_issues
    ORDER BY affected_records DESC
""").fetchdf()

print("Quality issues table created.")
print(result.to_string(index=False))

connection.close()