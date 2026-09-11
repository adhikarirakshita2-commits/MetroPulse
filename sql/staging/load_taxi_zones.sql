CREATE OR REPLACE TABLE dim_taxi_zone AS
SELECT
    LocationID AS location_id,
    Borough AS borough,
    Zone AS zone_name,
    service_zone
FROM read_csv_auto('data/raw/taxi_zone_lookup.csv');