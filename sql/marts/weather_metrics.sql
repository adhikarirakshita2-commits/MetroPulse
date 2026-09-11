CREATE OR REPLACE TABLE mart_weather_metrics AS
SELECT
    CASE
        WHEN precipitation = 0 THEN 'No Rain'
        WHEN precipitation < 2.5 THEN 'Light Rain'
        ELSE 'Heavy Rain'
    END AS precipitation_group,
    COUNT(*) AS hours,
    SUM(trips) AS trips,
    AVG(trips) AS avg_hourly_trips,
    AVG(avg_amount) AS avg_amount,
    AVG(temperature) AS avg_temperature,
    AVG(humidity) AS avg_humidity,
    AVG(wind_speed) AS avg_wind_speed
FROM int_weather_analysis
GROUP BY precipitation_group
ORDER BY avg_hourly_trips DESC;