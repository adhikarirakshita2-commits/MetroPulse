CREATE OR REPLACE TABLE int_weather_analysis AS
SELECT
    DATE_TRUNC('hour', t.tpep_pickup_datetime) AS hour,
    COUNT(*) AS trips,
    SUM(t.passenger_count) AS passengers,
    AVG(t.total_amount) AS avg_amount,
    AVG(w.temperature_2m) AS temperature,
    AVG(w.relative_humidity_2m) AS humidity,
    AVG(w.precipitation) AS precipitation,
    AVG(w.wind_speed_10m) AS wind_speed,
    MAX(w.weather_code) AS weather_code
FROM int_taxi_trips t
LEFT JOIN dim_weather w
    ON DATE_TRUNC('hour', t.tpep_pickup_datetime) = w.weather_time
WHERE t.usable_for_core_metrics = 1
GROUP BY hour
ORDER BY hour;