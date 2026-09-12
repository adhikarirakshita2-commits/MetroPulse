# MetroPulse Executive Decision Memo

## Decision

Run two four-week operational pilots:

1. Airport-focused driver supply and pricing operations.
2. Targeted driver-supply incentives for high-demand zone-hours.

The pilots should be evaluated using controlled treatment and comparison groups before any wider rollout.

## Executive Summary

The MetroPulse analysis covers NYC Yellow Taxi trips from April 1 through June 30, 2024.

The dataset contains 10,777,291 records in the required period. After applying the documented core-quality rules, 10,348,520 records are usable for core KPI calculations.

The strongest opportunity is airport operations. Airport-involved trips represent 10.00% of usable trips but account for 27.52% of total charged amount. Their average charged amount is $78.88 compared with $23.09 for non-airport trips.

Demand is also concentrated in specific locations and times. The top 10 pickup zones account for 37.48% of usable trips. The busiest single hour is 18:00, with 735,820 trips.

## Recommendation 1: Airport Operations

Run a four-week pilot targeting driver supply during high-demand airport windows.

Evidence:

* 1,035,243 airport-involved trips.
* 10.00% of usable trips.
* $81.66 million in charged amount.
* 27.52% of total charged amount.
* $78.88 average charged amount per trip.
* $23.09 average charged amount per non-airport trip.
* Average daily airport trip amount was $78.86 compared with $23.03 for non-airport trips.
* Difference in average daily airport versus non-airport trip amount: $55.83.
* 95% bootstrap confidence interval: $55.61 to $56.04.
* Permutation test: p < 0.001.

Pilot design:

* Unit: Airport pickup/dropoff zone by hour.
* Treatment: Targeted driver supply incentives during selected high-demand airport windows.
* Control: Comparable airport windows without the incentive.
* Primary metric: Completed airport trips per available driver-hour.
* MDE: Detect a 5% improvement in completed trips per available driver-hour.
* Sample-size reasoning: The pilot should be sized using the observed baseline variability and a 5% minimum detectable improvement, with enough zone-hour observations to provide adequate precision for the primary metric.
* Guardrails: Passenger wait time, cancellation rate, driver earnings, average trip amount and incentive cost.
* Stopping rule: Stop or modify the pilot if predefined guardrails deteriorate beyond acceptable limits.
* Decision: Expand if the primary metric improves and guardrails remain within acceptable limits.

## Recommendation 2: High-Demand Zone-Hour Supply

Run a four-week pilot using targeted driver incentives in selected high-demand zone-hours.

Evidence:

* Top 10 pickup zones account for 37.48% of usable trips.
* The busiest hour is 18:00 with 735,820 trips.
* Average daily demand is 113,720 trips.
* Daily demand ranges from 69,440 to 138,459 trips.
* Daily coefficient of variation is 12.44%.
* Thursday averages 127,182 trips compared with 95,881 on Monday.
* Thursday-Monday difference: 31,301 trips per day.
* 95% bootstrap confidence interval: 24,895 to 38,057 trips.
* Permutation test: p < 0.001.

Pilot design:

* Unit: Zone-hour.
* Treatment: Targeted driver incentives in selected high-demand zone-hours.
* Control: Similar zone-hours without the incentive.
* Primary metric: Completed trips per available driver-hour.
* MDE: Detect a 5% improvement in completed trips per available driver-hour.
* Sample-size reasoning: The pilot should be sized using the observed baseline variability and a 5% minimum detectable improvement, with enough zone-hour observations to provide adequate precision for the primary metric.
* Guardrails: Passenger wait time, cancellation rate, driver earnings and incentive cost per trip.
* Stopping rule: Stop or modify the pilot if predefined guardrails deteriorate beyond acceptable limits.
* Decision: Expand if trip productivity improves without unacceptable guardrail deterioration.

## Data Quality and Risk

The required-period dataset contains 10,777,291 records.

428,771 records, or 3.98%, are excluded from core KPI calculations because of documented material quality issues.

The excluded records represent:

* 1.46% of total charged amount.
* 3.45% of total trip distance.

Average charged amount changes from $27.94 before quality exclusions to $28.67 after exclusions.

This shows that data-quality treatment has a measurable effect on reported KPIs.

## Statistical Interpretation

The statistical tests establish differences in the observed data but do not establish causality.

The airport and demand findings should therefore be treated as evidence for testing operational interventions, not proof that incentives will cause higher demand or revenue.

The analysis includes bootstrap confidence intervals and permutation tests. Sensitivity is also checked using median trip amounts for the airport comparison.

## Weather Finding

Rainy hours showed higher observed taxi demand than dry hours in the analysis.

However, weather is correlated with time and day patterns, so this result should not be interpreted as a causal weather effect.

## Important Limitation

The required MTA Subway Hourly Ridership source could not be retrieved programmatically because the official public data endpoint returned access errors during the project.

No substitute or fabricated MTA data was used.

Therefore, the transit-linked portion of the analysis remains an outstanding limitation.

## Final Decision

Proceed with both four-week pilots rather than immediate full-scale rollout.

The pilots are reversible and provide a way to test whether the observed airport and zone-hour patterns translate into measurable operational improvement.

The final decision after four weeks should be based on the primary metrics, guardrails and predefined stopping rules.
