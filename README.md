# MetroPulse

MetroPulse is an urban mobility analytics project focused on understanding New York City taxi demand, trip economics, geographic concentration, airport activity, payment behavior, weather patterns, and data quality.

The analysis covers April 1, 2024 through June 30, 2024 using official public data sources.

## Live Dashboard

https://metropulse-2h2ccdgxnetip2ckhg36vf.streamlit.app/

The dashboard contains six views:

1. Executive Overview
2. Demand & Time
3. Geographic / Zones
4. Airport
5. Payment & Tipping
6. Weather & Data Quality

## Project Period

April 1, 2024 through June 30, 2024.

## Data Sources

### NYC TLC Yellow Taxi Trip Data

Official NYC Taxi and Limousine Commission monthly Parquet files were used for:

- April 2024
- May 2024
- June 2024

Source:
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

### NYC Taxi Zone Data

The official TLC taxi zone lookup table and taxi zone shapefile were used to identify pickup and dropoff zones.

Source:
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

### Weather

Historical hourly weather data was obtained from Open-Meteo for New York City.

Variables used include:

- Temperature
- Relative humidity
- Precipitation
- Wind speed
- Weather code

Source:
https://open-meteo.com/

### MTA Subway Ridership

The required MTA Subway Hourly Ridership 2020–2024 dataset was identified as dataset `wujg-7c2s`.

During development, the official public API/export endpoints returned access errors. No substitute dataset was fabricated or used. Therefore, the subway analysis is documented as a limitation rather than presenting unsupported results.

## Data Pipeline

The project follows a reproducible pipeline:

1. Download official source data programmatically.
2. Preserve raw source files.
3. Record source metadata.
4. Load taxi data into DuckDB.
5. Filter records to the required analysis period.
6. Apply data-quality rules.
7. Create staging and intermediate transformations.
8. Load taxi zone dimensions.
9. Load historical weather data.
10. Build analytical marts.
11. Run automated data-quality tests.
12. Run statistical and business analysis.
13. Build the dashboard from the analytical dashboard database.

## Project Structure

```text
MetroPulse/
│
├── analysis/
│   ├── anomaly_impact.py
│   ├── recommendations.py
│   ├── statistical_analysis.py
│   └── statistical_airport.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── samples/
│   └── processed/
│       └── dashboard.duckdb
│
├── ingestion/
│   ├── build_database.py
│   ├── build_dashboard_database.py
│   ├── download_taxi.py
│   ├── download_weather.py
│   ├── download_zones.py
│   ├── load_taxi_zones.py
│   ├── metadata.py
│   └── run_marts.py
│
├── sql/
│   ├── staging/
│   ├── intermediate/
│   └── marts/
│
├── tests/
│   └── test_data_quality.py
│
├── AI_USAGE.md
├── EXECUTIVE_MEMO.md
├── METRIC_DICTIONARY.md
├── README_DATA_QUALITY.md
├── README.md
└── requirements.txt