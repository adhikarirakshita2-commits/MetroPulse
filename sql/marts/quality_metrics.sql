CREATE OR REPLACE TABLE mart_quality_issues AS

SELECT
    'Invalid timestamps' AS issue,
    COUNT(*) AS affected_records,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM int_taxi_trips), 2) AS affected_percent
FROM int_taxi_trips
WHERE tpep_dropoff_datetime <= tpep_pickup_datetime

UNION ALL

SELECT
    'Zero or negative distance',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM int_taxi_trips), 2)
FROM int_taxi_trips
WHERE trip_distance <= 0

UNION ALL

SELECT
    'Invalid passenger count',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM int_taxi_trips), 2)
FROM int_taxi_trips
WHERE passenger_count <= 0

UNION ALL

SELECT
    'Zero or negative fare',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM int_taxi_trips), 2)
FROM int_taxi_trips
WHERE fare_amount <= 0

UNION ALL

SELECT
    'Negative total amount',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM int_taxi_trips), 2)
FROM int_taxi_trips
WHERE total_amount < 0

UNION ALL

SELECT
    'Negative tip amount',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM int_taxi_trips), 2)
FROM int_taxi_trips
WHERE tip_amount < 0

UNION ALL

SELECT
    'Very long trips',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM int_taxi_trips), 2)
FROM int_taxi_trips
WHERE trip_distance > 100

UNION ALL

SELECT
    'Very high trip speed',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM int_taxi_trips), 2)
FROM int_taxi_trips
WHERE speed_mph > 80

UNION ALL

SELECT
    'Suspicious fare vs total',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM int_taxi_trips), 2)
FROM int_taxi_trips
WHERE total_amount < fare_amount

UNION ALL

SELECT
    'Unknown payment type',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM int_taxi_trips), 2)
FROM int_taxi_trips
WHERE payment_type = 0;