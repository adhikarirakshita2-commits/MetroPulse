import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="MetroPulse",
    page_icon="🚕",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "processed" / "metropulse.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

st.title("🚕 MetroPulse")
st.caption("NYC Yellow Taxi Mobility Intelligence | April 1 – June 30, 2024")

st.sidebar.header("Filters")

start_date = st.sidebar.date_input(
    "Start date",
    pd.Timestamp("2024-04-01")
)

end_date = st.sidebar.date_input(
    "End date",
    pd.Timestamp("2024-06-30")
)

if start_date > end_date:
    st.error("Start date must be before or equal to end date.")
    st.stop()

start_date = str(start_date)
end_date = str(end_date)


def load_data(query, params=None):
    return con.execute(query, params or []).df()


daily = load_data(
    """
    SELECT *
    FROM mart_daily_metrics
    WHERE pickup_date BETWEEN ? AND ?
    ORDER BY pickup_date
    """,
    [start_date, end_date]
)

hourly = load_data(
    """
    SELECT *
    FROM mart_hourly_metrics
    ORDER BY pickup_hour
    """
)

zones = load_data(
    """
    SELECT
        z.pickup_zone_id,
        d.zone_name AS zone_name,
        z.trips,
        z.passengers,
        z.total_amount,
        z.avg_distance,
        z.avg_duration,
        z.avg_fare_per_mile
    FROM mart_zone_metrics z
    LEFT JOIN dim_taxi_zone d
        ON z.pickup_zone_id = d.location_id
    ORDER BY z.trips DESC
    """
)

if len(zones) > 0:
    zone_total_trips = zones["trips"].sum()
    zones["trip_share_pct"] = (
        zones["trips"] / zone_total_trips * 100
        if zone_total_trips
        else 0
    )

payment = load_data(
    """
    SELECT *
    FROM mart_payment_metrics
    ORDER BY trips DESC
    """
)

airport = load_data(
    """
    SELECT *
    FROM mart_airport_metrics
    ORDER BY airport_trip
    """
)

quality = load_data(
    """
    SELECT *
    FROM mart_quality_issues
    ORDER BY affected_records DESC
    """
)

weather = load_data(
    """
    SELECT *
    FROM mart_weather_metrics
    """
)

period_records = load_data(
    """
    SELECT COUNT(*) AS records
    FROM filtered_taxi_trips
    """
)["records"].iloc[0]

usable_records = load_data(
    """
    SELECT COUNT(*) AS records
    FROM int_taxi_trips
    WHERE usable_for_core_metrics = 1
    """
)["records"].iloc[0]

quality_excluded = period_records - usable_records

exclusion_rate = (
    quality_excluded / period_records * 100
    if period_records
    else 0
)

airport_trips = airport.loc[
    airport["airport_trip"] == 1,
    "trips"
].sum()

total_airport_trips = airport.loc[
    airport["airport_trip"] == 1,
    "trips"
].sum()

total_non_airport_trips = airport.loc[
    airport["airport_trip"] == 0,
    "trips"
].sum()

total_airport_amount = airport.loc[
    airport["airport_trip"] == 1,
    "total_amount"
].sum()

total_non_airport_amount = airport.loc[
    airport["airport_trip"] == 0,
    "total_amount"
].sum()

total_airport_trips_all = airport["trips"].sum()

airport_share = (
    airport_trips / total_airport_trips_all * 100
    if total_airport_trips_all
    else 0
)

airport_avg_amount = (
    total_airport_amount / total_airport_trips
    if total_airport_trips
    else 0
)

non_airport_avg_amount = (
    total_non_airport_amount / total_non_airport_trips
    if total_non_airport_trips
    else 0
)


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Executive Overview",
    "Demand & Time",
    "Zones",
    "Airport",
    "Payment & Tipping",
    "Weather & Quality"
])


with tab1:
    st.header("Executive Overview")

    total_trips = daily["trips"].sum()
    total_amount = daily["total_amount"].sum()

    avg_amount = (
        total_amount / total_trips
        if total_trips
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Trips",
        f"{total_trips:,.0f}"
    )

    c2.metric(
        "Total Charged",
        f"${total_amount:,.0f}"
    )

    c3.metric(
        "Average Trip Amount",
        f"${avg_amount:,.2f}"
    )

    c4.metric(
        "Airport Trip Share",
        f"{airport_share:.2f}%"
    )

    st.subheader("Daily Taxi Demand")

    st.line_chart(
        daily.set_index("pickup_date")["trips"]
    )

    st.subheader("Key Findings")

    st.write(
        "Airport-involved trips represent about 10% of usable trips "
        "but account for about 27.52% of total charged amount."
    )

    top_zone_share = (
        zones.head(10)["trip_share_pct"].sum()
        if "trip_share_pct" in zones.columns
        else 0
    )

    st.write(
        f"The top 10 pickup zones account for "
        f"{top_zone_share:.2f}% of usable trips."
    )

    st.write(
        f"{quality_excluded:,.0f} records "
        f"({exclusion_rate:.2f}%) are excluded from core KPI "
        "calculations because of documented data-quality issues."
    )


with tab2:
    st.header("Demand & Time")

    st.subheader("Trips by Hour")

    st.bar_chart(
        hourly.set_index("pickup_hour")["trips"]
    )

    st.subheader("Trips by Day of Week")

    day_data = load_data(
        """
        SELECT
            strftime(pickup_date, '%A') AS day_name,
            SUM(trips) AS trips
        FROM mart_daily_metrics
        WHERE pickup_date BETWEEN ? AND ?
        GROUP BY day_name
        ORDER BY trips DESC
        """,
        [start_date, end_date]
    )

    st.bar_chart(
        day_data.set_index("day_name")["trips"]
    )

    st.subheader("Daily Demand Statistics")

    avg_daily = daily["trips"].mean()
    min_daily = daily["trips"].min()
    max_daily = daily["trips"].max()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Daily Trips",
        f"{avg_daily:,.0f}"
    )

    c2.metric(
        "Minimum Daily Trips",
        f"{min_daily:,.0f}"
    )

    c3.metric(
        "Maximum Daily Trips",
        f"{max_daily:,.0f}"
    )


with tab3:
    st.header("Geographic / Zone Analysis")

    st.subheader("Top Pickup Zones")

    top_zones = zones.head(10).copy()

    st.bar_chart(
        top_zones.set_index("zone_name")["trips"]
    )

    top_zone_display = top_zones[
        [
            "zone_name",
            "trips",
            "trip_share_pct"
        ]
    ].copy()

    st.dataframe(
        top_zone_display,
        use_container_width=True
    )

    st.subheader("Zone Economics")

    zone_display = zones[
        [
            "zone_name",
            "trips",
            "trip_share_pct",
            "avg_distance",
            "avg_duration",
            "avg_fare_per_mile",
            "total_amount"
        ]
    ].head(20)

    st.dataframe(
        zone_display,
        use_container_width=True
    )


with tab4:
    st.header("Airport Analysis")

    airport_display = airport.copy()

    airport_display["type"] = airport_display[
        "airport_trip"
    ].map({
        1: "Airport-involved",
        0: "Non-airport"
    })

    airport_display = airport_display.set_index("type")

    st.bar_chart(
        airport_display["trips"]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Airport Trips",
        f"{total_airport_trips:,.0f}"
    )

    c2.metric(
        "Airport Trip Share",
        f"{airport_share:.2f}%"
    )

    c3.metric(
        "Airport Avg Amount",
        f"${airport_avg_amount:,.2f}"
    )

    c4.metric(
        "Airport Amount Premium",
        f"${airport_avg_amount - non_airport_avg_amount:,.2f}"
    )

    display_columns = [
        "trips",
        "total_amount",
        "avg_amount",
        "avg_distance",
        "avg_duration"
    ]

    st.dataframe(
        airport_display[display_columns],
        use_container_width=True
    )

    st.info(
        "Airport-involved means the pickup or dropoff location is "
        "one of the identified airport taxi zones."
    )


with tab5:
    st.header("Payment & Tipping")

    payment_display = payment.copy()

    if "payment_type" in payment_display.columns:
        payment_display["payment_type"] = (
            payment_display["payment_type"]
            .astype(str)
        )

    st.subheader("Trips by Payment Type")

    st.bar_chart(
        payment_display.set_index("payment_type")["trips"]
    )

    st.subheader("Payment Metrics")

    st.dataframe(
        payment_display,
        use_container_width=True
    )

    st.info(
        "Payment type 0 is treated as unknown or unclassified. "
        "It is not assumed to represent a specific payment method."
    )


with tab6:
    st.header("Weather & Data Quality")

    st.subheader("Taxi Demand by Rain Category")

    if "rain_category" in weather.columns:
        st.bar_chart(
            weather.set_index("rain_category")["trips"]
        )

    st.dataframe(
        weather,
        use_container_width=True
    )

    st.subheader("Data Quality Issues")

    quality_display = quality.copy()

    st.bar_chart(
        quality_display.set_index("issue")["affected_records"]
    )

    st.dataframe(
        quality_display,
        use_container_width=True
    )

    st.warning(
        "MTA Subway Hourly Ridership data could not be retrieved "
        "programmatically from the required official public endpoint. "
        "No substitute or fabricated transit data was used."
    )


st.divider()

st.caption(
    "Core KPI calculations use records passing the documented "
    "data-quality rules. Findings are observational and do not "
    "establish causality."
)

st.caption(
    "Data period: April 1 – June 30, 2024"
)

st.caption(
    f"Dashboard refresh: "
    f"{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
)