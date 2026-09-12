import duckdb

connection = duckdb.connect("data/processed/metropulse.duckdb")

airport_query = """
SELECT
    airport_trip,
    SUM(trips) AS trips,
    SUM(total_amount) AS total_amount,
    AVG(avg_amount) AS avg_amount
FROM mart_airport_metrics
GROUP BY airport_trip
ORDER BY airport_trip DESC
"""

airport = connection.execute(airport_query).fetchdf()

zone_query = """
SELECT
    zone_name,
    trips,
    trips * 100.0 / (SELECT SUM(trips) FROM int_zone_analysis) AS trip_share_percent,
    avg_distance,
    avg_duration,
    avg_fare_per_mile,
    total_amount
FROM int_zone_analysis
ORDER BY trips DESC
LIMIT 10
"""

zones = connection.execute(zone_query).fetchdf()

hour_query = """
SELECT
    pickup_hour,
    trips,
    demand_period
FROM mart_hourly_metrics
ORDER BY trips DESC
LIMIT 5
"""

hours = connection.execute(hour_query).fetchdf()

daily_query = """
SELECT
    AVG(trips) AS average_daily_trips,
    MIN(trips) AS minimum_daily_trips,
    MAX(trips) AS maximum_daily_trips,
    STDDEV(trips) * 100.0 / AVG(trips) AS coefficient_of_variation_percent
FROM mart_daily_metrics
"""

daily = connection.execute(daily_query).fetchone()

connection.close()

airport_trips = airport[airport["airport_trip"] == 1]["trips"].iloc[0]
airport_amount = airport[airport["airport_trip"] == 1]["total_amount"].iloc[0]
airport_avg = airport[airport["airport_trip"] == 1]["avg_amount"].iloc[0]
non_airport_avg = airport[airport["airport_trip"] == 0]["avg_amount"].iloc[0]

total_amount = airport["total_amount"].sum()
airport_amount_share = airport_amount * 100 / total_amount

top_10_share = zones["trip_share_percent"].sum()
busiest_hour = hours.iloc[0]

print("\nMETROPULSE BUSINESS RECOMMENDATIONS")
print("=" * 65)

print("\nINITIATIVE 1: AIRPORT-FOCUSED SUPPLY AND PRICING OPERATIONS")
print("-" * 65)
print(f"Airport-involved trips: {airport_trips:,.0f}")
print(f"Airport trip share: {airport_trips / airport['trips'].sum() * 100:.2f}%")
print(f"Airport total amount: ${airport_amount:,.2f}")
print(f"Airport share of total amount: {airport_amount_share:.2f}%")
print(f"Airport average amount: ${airport_avg:.2f}")
print(f"Non-airport average amount: ${non_airport_avg:.2f}")
print(f"Airport amount premium: ${airport_avg - non_airport_avg:.2f}")

print("\n4-WEEK PILOT")
print("Unit: Airport pickup/dropoff zone by hour")
print("Treatment: Targeted driver supply incentives during high-demand airport windows")
print("Control: Comparable airport windows without the incentive")
print("Primary metric: Completed airport trips per available driver-hour")
print("Guardrails: Average trip amount, cancellation rate, driver earnings, passenger wait time")
print("MDE approach: Detect a 5% improvement in completed trips per driver-hour")
print("Stopping rule: Stop if guardrail deterioration exceeds the predefined threshold")
print("Decision rule: Scale if the primary metric improves without guardrail failure")

print("\nINITIATIVE 2: DRIVER-SUPPLY INCENTIVES FOR HIGH-DEMAND ZONES AND HOURS")
print("-" * 65)
print(f"Top 10 pickup zones share: {top_10_share:.2f}% of usable trips")
print(f"Busiest hour: {int(busiest_hour['pickup_hour'])}:00")
print(f"Busiest-hour trips: {busiest_hour['trips']:,.0f}")
print(f"Average daily trips: {daily[0]:,.0f}")
print(f"Minimum daily trips: {daily[1]:,.0f}")
print(f"Maximum daily trips: {daily[2]:,.0f}")
print(f"Daily demand coefficient of variation: {daily[3]:.2f}%")

print("\n4-WEEK PILOT")
print("Unit: Zone-hour")
print("Treatment: Targeted driver incentives in selected high-demand zone-hours")
print("Control: Similar zone-hours without the incentive")
print("Primary metric: Completed trips per available driver-hour")
print("Guardrails: Driver earnings, passenger wait time, cancellation rate, incentive cost per trip")
print("MDE approach: Detect a 5% improvement in completed trips per driver-hour")
print("Stopping rule: Stop if wait time, cancellations, or incentive cost breach guardrails")
print("Decision rule: Scale if trip productivity improves and unit economics remain acceptable")

print("\nLIMITATIONS")
print("-" * 65)
print("The analysis is observational and does not establish causality.")
print("Airport-involved trips include trips with either airport pickup or airport dropoff.")
print("The MTA subway dataset could not be retrieved because the official public endpoint returned access errors.")
print("Pilot results should therefore be validated through controlled experimentation.")