CREATE OR REPLACE TABLE mart_daily_metrics AS
SELECT
    pickup_date,
    COUNT(*) AS trips,
    SUM(passenger_count) AS passengers,
    SUM(trip_distance) AS total_distance,
    SUM(fare_amount) AS total_fare,
    SUM(total_amount) AS total_amount,
    AVG(trip_distance) AS avg_distance,
    AVG(trip_duration_minutes) AS avg_duration,
    MEDIAN(trip_duration_minutes) AS median_duration,
    AVG(fare_per_mile) AS avg_fare_per_mile,
    AVG(amount_per_minute) AS avg_amount_per_minute
FROM int_taxi_trips
WHERE usable_for_core_metrics = 1
GROUP BY pickup_date
ORDER BY pickup_date;

CREATE OR REPLACE TABLE mart_hourly_metrics AS
SELECT
    pickup_hour,
    demand_period,
    COUNT(*) AS trips,
    SUM(passenger_count) AS passengers,
    AVG(trip_distance) AS avg_distance,
    AVG(trip_duration_minutes) AS avg_duration,
    AVG(total_amount) AS avg_amount
FROM int_taxi_trips
WHERE usable_for_core_metrics = 1
GROUP BY pickup_hour, demand_period
ORDER BY pickup_hour;

CREATE OR REPLACE TABLE mart_zone_metrics AS
SELECT
    PULocationID AS pickup_zone_id,
    COUNT(*) AS trips,
    SUM(passenger_count) AS passengers,
    SUM(total_amount) AS total_amount,
    AVG(trip_distance) AS avg_distance,
    AVG(trip_duration_minutes) AS avg_duration,
    AVG(fare_per_mile) AS avg_fare_per_mile
FROM int_taxi_trips
WHERE usable_for_core_metrics = 1
GROUP BY PULocationID
ORDER BY trips DESC;

CREATE OR REPLACE TABLE mart_payment_metrics AS
SELECT
    payment_type,
    COUNT(*) AS trips,
    SUM(total_amount) AS total_amount,
    AVG(total_amount) AS avg_amount,
    AVG(tip_amount) AS avg_tip,
    AVG(tip_rate_percent) AS avg_tip_rate
FROM int_taxi_trips
WHERE usable_for_core_metrics = 1
GROUP BY payment_type
ORDER BY trips DESC;

CREATE OR REPLACE TABLE mart_airport_metrics AS
SELECT
    airport_trip,
    COUNT(*) AS trips,
    SUM(total_amount) AS total_amount,
    AVG(total_amount) AS avg_amount,
    AVG(trip_distance) AS avg_distance,
    AVG(trip_duration_minutes) AS avg_duration
FROM int_taxi_trips
WHERE usable_for_core_metrics = 1
GROUP BY airport_trip
ORDER BY airport_trip;

CREATE OR REPLACE TABLE mart_quality_metrics AS
SELECT
    data_quality_status,
    COUNT(*) AS trips
FROM int_taxi_trips
GROUP BY data_quality_status
ORDER BY trips DESC;

CREATE OR REPLACE TABLE mart_day_metrics AS
SELECT
    pickup_day,
    COUNT(*) AS trips,
    SUM(total_amount) AS total_amount,
    AVG(total_amount) AS avg_amount,
    AVG(trip_duration_minutes) AS avg_duration,
    AVG(trip_distance) AS avg_distance
FROM int_taxi_trips
WHERE usable_for_core_metrics = 1
GROUP BY pickup_day
ORDER BY trips DESC;