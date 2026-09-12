import duckdb
import numpy as np

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    pickup_date,
    trips,
    DAYNAME(pickup_date) AS day_name
FROM mart_daily_metrics
ORDER BY pickup_date
"""

data = connection.execute(query).fetchdf()
connection.close()

thursday = data[data["day_name"] == "Thursday"]["trips"].to_numpy()
monday = data[data["day_name"] == "Monday"]["trips"].to_numpy()

observed_difference = thursday.mean() - monday.mean()

rng = np.random.default_rng(42)

bootstrap_differences = []

for _ in range(10000):
    thursday_sample = rng.choice(thursday, size=len(thursday), replace=True)
    monday_sample = rng.choice(monday, size=len(monday), replace=True)

    difference = thursday_sample.mean() - monday_sample.mean()
    bootstrap_differences.append(difference)

bootstrap_differences = np.array(bootstrap_differences)

lower_ci = np.percentile(bootstrap_differences, 2.5)
upper_ci = np.percentile(bootstrap_differences, 97.5)

combined = np.concatenate([thursday, monday])

permutation_differences = []

for _ in range(10000):
    shuffled = rng.permutation(combined)

    shuffled_thursday = shuffled[:len(thursday)]
    shuffled_monday = shuffled[len(thursday):]

    difference = shuffled_thursday.mean() - shuffled_monday.mean()
    permutation_differences.append(difference)

permutation_differences = np.array(permutation_differences)

p_value = np.mean(
    np.abs(permutation_differences) >= abs(observed_difference)
)

print("\nTHURSDAY VS MONDAY DAILY DEMAND")
print("-" * 50)
print(f"Thursday days: {len(thursday)}")
print(f"Monday days: {len(monday)}")
print(f"Average Thursday trips: {thursday.mean():,.0f}")
print(f"Average Monday trips: {monday.mean():,.0f}")
print(f"Observed difference: {observed_difference:,.0f} trips")
print(f"95% bootstrap CI: {lower_ci:,.0f} to {upper_ci:,.0f} trips")
print(f"Permutation p-value: {p_value:.4f}")

if p_value < 0.05:
    print("Result: Statistically significant difference")
else:
    print("Result: Not statistically significant")