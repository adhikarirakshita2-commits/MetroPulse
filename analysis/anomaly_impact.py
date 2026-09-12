import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

query = """
SELECT
    COUNT(*) AS total_records,
    SUM(total_amount) AS total_amount,
    AVG(total_amount) AS avg_amount,
    SUM(trip_distance) AS total_distance
FROM filtered_taxi_trips
"""

all_data = connection.execute(query).fetchone()

query = """
SELECT
    COUNT(*) AS usable_records,
    SUM(total_amount) AS total_amount,
    AVG(total_amount) AS avg_amount,
    SUM(trip_distance) AS total_distance
FROM int_taxi_trips
WHERE usable_for_core_metrics = 1
"""

usable_data = connection.execute(query).fetchone()

total_records = all_data[0]
total_amount = all_data[1]
avg_amount = all_data[2]
total_distance = all_data[3]

usable_records = usable_data[0]
usable_amount = usable_data[1]
usable_avg_amount = usable_data[2]
usable_distance = usable_data[3]

excluded_records = total_records - usable_records
excluded_amount = total_amount - usable_amount
excluded_distance = total_distance - usable_distance

trip_impact = excluded_records * 100 / total_records
amount_impact = excluded_amount * 100 / total_amount
distance_impact = excluded_distance * 100 / total_distance
avg_amount_difference = avg_amount - usable_avg_amount

print("\nANOMALY IMPACT ON CORE KPIs")
print("-" * 55)
print(f"Period records: {total_records:,.0f}")
print(f"Usable records: {usable_records:,.0f}")
print(f"Excluded records: {excluded_records:,.0f}")
print(f"Excluded record share: {trip_impact:.2f}%")
print()
print(f"All-record total amount: ${total_amount:,.2f}")
print(f"Usable total amount: ${usable_amount:,.2f}")
print(f"Excluded amount share: {amount_impact:.2f}%")
print()
print(f"All-record average amount: ${avg_amount:.2f}")
print(f"Usable average amount: ${usable_avg_amount:.2f}")
print(f"Average amount difference: ${avg_amount_difference:.2f}")
print()
print(f"All-record total distance: {total_distance:,.2f}")
print(f"Usable total distance: {usable_distance:,.2f}")
print(f"Excluded distance share: {distance_impact:.2f}%")

connection.close()