import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    CASE
        WHEN tpep_pickup_datetime < '2024-04-01'
            THEN 'Before April 1'
        ELSE 'After June 30'
    END AS period_issue,
    COUNT(*) AS records
FROM stg_taxi_trips
WHERE tpep_pickup_datetime < '2024-04-01'
   OR tpep_pickup_datetime >= '2024-07-01'
GROUP BY period_issue
ORDER BY period_issue
"""

result = connection.execute(query).fetchdf()

print(result.to_string(index=False))

connection.close()