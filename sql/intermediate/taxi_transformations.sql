CREATE OR REPLACE TABLE filtered_taxi_trips AS
SELECT *
FROM clean_taxi_trips
WHERE tpep_pickup_datetime >= '2024-04-01'
  AND tpep_pickup_datetime < '2024-07-01';

CREATE OR REPLACE TABLE int_trip_duration AS
SELECT
    *,
    EXTRACT(EPOCH FROM
        (tpep_dropoff_datetime - tpep_pickup_datetime)
    ) / 60 AS trip_duration_minutes
FROM filtered_taxi_trips;

CREATE OR REPLACE TABLE int_trip_speed AS
SELECT
    *,
    CASE
        WHEN trip_duration_minutes > 0
        THEN trip_distance / (trip_duration_minutes / 60)
        ELSE NULL
    END AS speed_mph
FROM int_trip_duration;

CREATE OR REPLACE TABLE int_trip_date AS
SELECT
    *,
    CAST(tpep_pickup_datetime AS DATE) AS pickup_date
FROM int_trip_speed;

CREATE OR REPLACE TABLE int_trip_hour AS
SELECT
    *,
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickup_hour
FROM int_trip_date;

CREATE OR REPLACE TABLE int_trip_day AS
SELECT
    *,
    DAYNAME(tpep_pickup_datetime) AS pickup_day
FROM int_trip_hour;

CREATE OR REPLACE TABLE int_peak_classification AS
SELECT
    *,
    CASE
        WHEN pickup_hour IN (7, 8, 9, 16, 17, 18, 19)
        THEN 'Peak'
        ELSE 'Off-Peak'
    END AS demand_period
FROM int_trip_day;

CREATE OR REPLACE TABLE int_fare_per_mile AS
SELECT
    *,
    CASE
        WHEN trip_distance > 0
        THEN fare_amount / trip_distance
        ELSE NULL
    END AS fare_per_mile
FROM int_peak_classification;

CREATE OR REPLACE TABLE int_amount_per_minute AS
SELECT
    *,
    CASE
        WHEN trip_duration_minutes > 0
        THEN total_amount / trip_duration_minutes
        ELSE NULL
    END AS amount_per_minute
FROM int_fare_per_mile;

CREATE OR REPLACE TABLE int_tip_rate AS
SELECT
    *,
    CASE
        WHEN fare_amount > 0
        THEN (tip_amount / fare_amount) * 100
        ELSE NULL
    END AS tip_rate_percent
FROM int_amount_per_minute;

CREATE OR REPLACE TABLE int_airport_flag AS
SELECT
    *,
    CASE
        WHEN PULocationID IN (1, 132, 138)
          OR DOLocationID IN (1, 132, 138)
        THEN 1
        ELSE 0
    END AS airport_trip
FROM int_tip_rate;

CREATE OR REPLACE TABLE int_analysis_flag AS
SELECT
    *,
    CASE
        WHEN data_quality_status = 'valid'
        THEN 1
        ELSE 0
    END AS usable_for_core_metrics
FROM int_airport_flag;

CREATE OR REPLACE TABLE int_taxi_trips AS
SELECT
    VendorID,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    pickup_date,
    pickup_hour,
    pickup_day,
    demand_period,
    passenger_count,
    trip_distance,
    trip_duration_minutes,
    speed_mph,
    PULocationID,
    DOLocationID,
    payment_type,
    fare_amount,
    tip_amount,
    total_amount,
    fare_per_mile,
    amount_per_minute,
    tip_rate_percent,
    airport_trip,
    data_quality_status,
    usable_for_core_metrics
FROM int_analysis_flag;