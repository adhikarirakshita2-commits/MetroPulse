import duckdb
import numpy as np

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    pickup_date,
    airport_trip,
    COUNT(*) AS trips,
    AVG(total_amount) AS avg_amount,
    MEDIAN(total_amount) AS median_amount
FROM int_taxi_trips
WHERE usable_for_core_metrics = 1
GROUP BY pickup_date, airport_trip
ORDER BY pickup_date, airport_trip
"""

data = connection.execute(query).fetchdf()
connection.close()

airport = data[data["airport_trip"] == 1].set_index("pickup_date")
non_airport = data[data["airport_trip"] == 0].set_index("pickup_date")

matched = airport.join(
    non_airport,
    lsuffix="_airport",
    rsuffix="_non_airport"
)

mean_differences = (
    matched["avg_amount_airport"]
    - matched["avg_amount_non_airport"]
).to_numpy()

median_differences = (
    matched["median_amount_airport"]
    - matched["median_amount_non_airport"]
).to_numpy()

observed_mean_difference = mean_differences.mean()
observed_median_difference = median_differences.mean()

rng = np.random.default_rng(42)

bootstrap_mean = []
bootstrap_median = []

for _ in range(10000):
    sample = rng.choice(
        mean_differences,
        size=len(mean_differences),
        replace=True
    )
    bootstrap_mean.append(sample.mean())

    sample = rng.choice(
        median_differences,
        size=len(median_differences),
        replace=True
    )
    bootstrap_median.append(sample.mean())

bootstrap_mean = np.array(bootstrap_mean)
bootstrap_median = np.array(bootstrap_median)

mean_lower = np.percentile(bootstrap_mean, 2.5)
mean_upper = np.percentile(bootstrap_mean, 97.5)

median_lower = np.percentile(bootstrap_median, 2.5)
median_upper = np.percentile(bootstrap_median, 97.5)

permutation_results = []

for _ in range(10000):
    signs = rng.choice([-1, 1], size=len(mean_differences))
    permutation_results.append(
        np.mean(mean_differences * signs)
    )

permutation_results = np.array(permutation_results)

p_value = np.mean(
    np.abs(permutation_results) >= abs(observed_mean_difference)
)

airport_total_trips = data[data["airport_trip"] == 1]["trips"].sum()
non_airport_total_trips = data[data["airport_trip"] == 0]["trips"].sum()

airport_amount = data[data["airport_trip"] == 1]["avg_amount"].mean()
non_airport_amount = data[data["airport_trip"] == 0]["avg_amount"].mean()

print("\nAIRPORT VS NON-AIRPORT TRIP ECONOMICS")
print("-" * 55)
print(f"Airport trips: {airport_total_trips:,.0f}")
print(f"Non-airport trips: {non_airport_total_trips:,.0f}")
print(f"Average daily airport amount: ${airport_amount:.2f}")
print(f"Average daily non-airport amount: ${non_airport_amount:.2f}")
print(f"Average daily mean-amount difference: ${observed_mean_difference:.2f}")
print(f"95% bootstrap CI for mean difference: ${mean_lower:.2f} to ${mean_upper:.2f}")
print(f"Average daily median-amount difference: ${observed_median_difference:.2f}")
print(f"95% bootstrap CI for median difference: ${median_lower:.2f} to ${median_upper:.2f}")
print(f"Permutation p-value: {p_value:.4f}")

if p_value < 0.05:
    print("Result: Statistically significant difference")
else:
    print("Result: Not statistically significant")