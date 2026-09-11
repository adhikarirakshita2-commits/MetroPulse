CREATE OR REPLACE TABLE int_destination_zone_analysis AS
SELECT
    t.DOLocationID AS dropoff_zone_id,
    z.borough,
    z.zone_name,
    z.service_zone,
    COUNT(*) AS trips,
    SUM(t.passenger_count) AS passengers,
    SUM(t.total_amount) AS total_amount,
    AVG(t.trip_distance) AS avg_distance,
    AVG(t.trip_duration_minutes) AS avg_duration
FROM int_taxi_trips t
LEFT JOIN dim_taxi_zone z
    ON t.DOLocationID = z.location_id
WHERE t.usable_for_core_metrics = 1
GROUP BY
    t.DOLocationID,
    z.borough,
    z.zone_name,
    z.service_zone
ORDER BY trips DESC;