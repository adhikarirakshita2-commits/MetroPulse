# MetroPulse Data Quality Rules

## Data quality approach

MetroPulse preserves the original taxi records in the raw and staging layers. Records are not deleted from the source data because the original data must remain reproducible.

Records with material quality problems are identified and labelled in the analytical layer.

## Records excluded from core metrics

The following records are excluded from core KPI calculations:

- Invalid pickup or dropoff timestamps
- Zero or negative trip distance
- Zero or negative passenger count
- Zero or negative fare amount
- Negative total amount
- Negative tip amount

These records remain available in the staging and analytical data for quality analysis.

## Records retained with labels

Records with the following conditions are retained and labelled for investigation:

- Very high trip speed
- Very long trip distance
- Suspicious relationship between fare amount and total amount
- Unknown payment type

These conditions can represent unusual but potentially legitimate trips, so they are not automatically removed from the dataset.

## Payment information

Payment type 0 is treated as unknown or unclassified payment information.

These records remain in the dataset but are not interpreted as a specific payment method.

## Duplicate records

Exact duplicate groups were checked using key trip attributes including vendor, pickup time, dropoff time, passenger count, distance, pickup zone, dropoff zone, fare and total amount.

No exact duplicate groups were detected.

## Zone information

Pickup and dropoff zone IDs are checked against the official NYC TLC taxi zone lookup.

Records with unmatched zones are monitored separately.

## Period filtering

The required analysis period is April 1, 2024 through June 30, 2024.

Records outside this period are retained in the staging layer but excluded from the analytical period.

## Core metric rule

The `usable_for_core_metrics` field identifies records that meet the core quality rules.

Core KPI calculations use only records where:

`usable_for_core_metrics = 1`

This prevents questionable records from distorting the main business metrics while preserving them for quality investigation.