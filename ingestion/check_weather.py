import pandas as pd

weather = pd.read_csv("data/raw/nyc_weather_2024-04_to_2024-06.csv")

weather["time"] = pd.to_datetime(weather["time"])

print("First timestamp:", weather["time"].min())
print("Last timestamp:", weather["time"].max())
print("Missing values:")
print(weather.isna().sum())