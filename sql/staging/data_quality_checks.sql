SELECT
    COUNT(*) AS invalid_timestamp_trips
FROM stg_taxi_trips
WHERE tpep_dropoff_datetime <= tpep_pickup_datetime;
SELECT
    COUNT(*) AS invalid_distance_trips
FROM stg_taxi_trips
WHERE trip_distance <= 0;