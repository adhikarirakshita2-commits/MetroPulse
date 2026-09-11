CREATE OR REPLACE TABLE clean_taxi_trips AS
SELECT
    *,
    
    CASE
        WHEN tpep_dropoff_datetime <= tpep_pickup_datetime
            THEN 'invalid_timestamp'
        WHEN trip_distance <= 0
            THEN 'invalid_distance'
        WHEN passenger_count <= 0
            THEN 'invalid_passenger_count'
        WHEN fare_amount <= 0
            THEN 'invalid_fare'
        WHEN total_amount < 0
            THEN 'invalid_total_amount'
        WHEN tip_amount < 0
            THEN 'invalid_tip'
        ELSE 'valid'
    END AS data_quality_status

FROM stg_taxi_trips;