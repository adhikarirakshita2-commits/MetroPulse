# MetroPulse Metric Dictionary

## Scope

All core metrics use the required analysis period:

April 1, 2024 through June 30, 2024.

Core KPI calculations use records where:

`usable_for_core_metrics = 1`

The raw and staging data remain preserved separately.

## Trips

Definition:

Count of taxi trip records.

Calculation:

`COUNT(*)`

Source:

`int_taxi_trips`

Core rule:

Only records with `usable_for_core_metrics = 1` are included in core KPI calculations.

## Passengers

Definition:

Sum of passenger counts reported in taxi trip records.

Calculation:

`SUM(passenger_count)`

Unit:

Reported passenger count.

Caution:

Passenger count contains quality issues and should be interpreted as reported passenger information rather than independently verified occupancy.

## Total Charged Amount

Definition:

Sum of `total_amount` across usable taxi trips.

Calculation:

`SUM(total_amount)`

Unit:

USD.

## Total Fare

Definition:

Sum of the taxi meter fare amount across usable trips.

Calculation:

`SUM(fare_amount)`

Unit:

USD.

## Total Distance

Definition:

Sum of reported taxi trip distance.

Calculation:

`SUM(trip_distance)`

Unit:

Miles.

## Average Trip Amount

Definition:

Average charged amount per usable taxi trip.

Calculation:

`AVG(total_amount)`

Unit:

USD per trip.

## Median Trip Amount

Definition:

Median charged amount per usable taxi trip.

Calculation:

`MEDIAN(total_amount)`

Unit:

USD per trip.

Median is used as a sensitivity measure because trip amounts are not necessarily normally distributed.

## Trip Amount Percentiles

Definition:

Selected percentile values of charged amount across usable taxi trips.

Calculation:

P50, P75, P90 and P95 of `total_amount`.

Unit:

USD per trip.

Percentiles are used to describe the distribution and reduce reliance on the average alone.

## Average Trip Distance

Definition:

Average reported distance per usable trip.

Calculation:

`AVG(trip_distance)`

Unit:

Miles.

## Average Trip Duration

Definition:

Average elapsed time between pickup and dropoff.

Calculation:

Average of:

`dropoff_datetime - pickup_datetime`

Unit:

Minutes.

## Fare Per Mile

Definition:

Meter fare divided by reported trip distance.

Calculation:

`fare_amount / trip_distance`

Unit:

USD per mile.

Trips with non-positive distance are excluded from core metrics.

## Amount Per Minute

Definition:

Total charged amount divided by trip duration.

Calculation:

`total_amount / trip_duration_minutes`

Unit:

USD per minute.

Trips with non-positive duration are excluded from this calculation.

## Tip Rate

Definition:

Tip amount as a percentage of fare amount.

Calculation:

`tip_amount / fare_amount * 100`

Unit:

Percent.

Cash and unknown payment records are not interpreted as equivalent to card tipping behavior.

## Airport-Involved Trip

Definition:

A trip where either the pickup or dropoff location is one of the identified airport taxi zones.

Airport zones used:

- LocationID 1
- LocationID 132
- LocationID 138

Calculation:

`airport_trip = 1`

Interpretation:

This metric represents airport-involved trips, not airport pickups only.

## Airport Trip Share

Definition:

Percentage of usable trips that are airport-involved.

Calculation:

`airport trips / total usable trips * 100`

## Peak Hour

Definition:

A pickup hour classified as Peak using the project demand-period rule.

Peak hours:

07:00, 08:00, 09:00, 16:00, 17:00, 18:00 and 19:00.

All other hours are classified as Off-Peak.

## Zone Trip Share

Definition:

Percentage of usable pickup trips originating from a zone.

Calculation:

`zone trips / total usable trips * 100`

## Daily Demand

Definition:

Number of usable taxi trips occurring on a calendar day.

Calculation:

`COUNT(*) GROUP BY pickup_date`

## Daily Demand Coefficient of Variation

Definition:

Standard deviation of daily trips divided by average daily trips.

Calculation:

`standard deviation / average * 100`

Unit:

Percent.

This measures relative day-to-day demand variability.

## Weather Demand

Definition:

Hourly usable taxi demand aligned to the corresponding Open-Meteo weather observation.

Join:

Taxi pickup timestamp truncated to the hour is matched with the weather timestamp.

Weather findings are observational and do not establish causality.

## Rain Category

Definitions:

- No Rain: precipitation = 0
- Light Rain: precipitation > 0 and < 2.5
- Heavy Rain: precipitation >= 2.5

Unit:

Millimetres of precipitation per hour.

## Data Quality Exclusion Rate

Definition:

Percentage of required-period records excluded from core KPI calculations.

Calculation:

`excluded records / required-period records * 100`

Observed value:

3.98%.

## Quality Exclusion Impact

Definition:

The difference between KPI results calculated using all required-period records and results calculated using usable records only.

The project reports the number and percentage of excluded records and their contribution to key measures such as total amount and total distance.

## Statistical Difference

Definition:

Difference between the average outcome of two comparison groups.

Example:

Thursday average daily trips minus Monday average daily trips.

## Bootstrap Confidence Interval

Definition:

A 95% interval estimated by repeatedly resampling the observed comparison data with replacement.

The project uses 10,000 bootstrap iterations.

## Permutation Test

Definition:

A resampling-based significance test that randomly reallocates observations between comparison groups to estimate how often a difference as large as the observed difference occurs under the null hypothesis.

The project uses 10,000 permutations.

## Statistical Significance

A comparison is labelled statistically significant when the permutation p-value is below 0.05.

Statistical significance does not imply causality or practical importance by itself.

## Usable Record

Definition:

A record that passes the project's core data-quality rules.

The following conditions cause exclusion from core KPI calculations:

- Invalid timestamp
- Zero or negative distance
- Invalid passenger count
- Zero or negative fare
- Negative total amount
- Negative tip amount

Questionable but potentially legitimate records such as very high speed, very long distance and unknown payment type remain available for investigation rather than automatically being removed.