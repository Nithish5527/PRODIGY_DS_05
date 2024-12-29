import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopandas import GeoDataFrame
from shapely.geometry import Point

# Load dataset
data_path = r"C:\Acc_Classified_according_to_Type_of_Weather_Condition_2014_and_2016.csv"
df = pd.read_csv(data_path)

# Display dataset overview
print("Dataset Preview:\n", df.head())
print("Available Columns:\n", df.columns)

# Specify columns of interest
columns_of_interest = [
    'Year', 'State/UT', 'Road_Type', 'Weather_Condition', 
    'Accidents', 'Fatalities', 'Injuries', 'Latitude', 'Longitude'
]

# Check for missing columns
missing_columns = [col for col in columns_of_interest if col not in df.columns]
if missing_columns:
    print(f"Missing columns: {missing_columns}")

# Filter dataset by available columns
columns_of_interest = [col for col in columns_of_interest if col in df.columns]
df = df[columns_of_interest]

# Handle missing data
columns_to_check = ['Weather_Condition', 'Latitude', 'Longitude']
df.dropna(subset=[col for col in columns_to_check if col in df.columns], inplace=True)

# Grouped analyses
time_analysis = df.groupby('Year')[['Accidents', 'Fatalities', 'Injuries']].sum() if 'Year' in df.columns else pd.DataFrame()
road_condition_analysis = df.groupby('Road_Type')[['Accidents', 'Fatalities', 'Injuries']].sum() if 'Road_Type' in df.columns else pd.DataFrame()
weather_analysis = df.groupby('Weather_Condition')[['Accidents', 'Fatalities', 'Injuries']].sum() if 'Weather_Condition' in df.columns else pd.DataFrame()

# Visualizations

# Yearly Trends
if not time_analysis.empty:
    time_analysis.plot(kind='line', marker='o', figsize=(10, 6))
    plt.title('Yearly Trends in Road Accidents, Fatalities, and Injuries')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Accidents by Road Type
if not road_condition_analysis.empty:
    road_condition_analysis['Accidents'].sort_values(ascending=False).plot(kind='bar', color='skyblue', figsize=(10, 6))
    plt.title('Accidents by Road Type')
    plt.xlabel('Road Type')
    plt.ylabel('Number of Accidents')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Accidents by Weather Condition
if not weather_analysis.empty:
    weather_analysis['Accidents'].sort_values(ascending=False).plot(kind='bar', color='orange', figsize=(10, 6))
    plt.title('Accidents by Weather Condition')
    plt.xlabel('Weather Condition')
    plt.ylabel('Number of Accidents')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Accident Hotspots
if 'Latitude' in df.columns and 'Longitude' in df.columns:
    gdf = GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df.Longitude, df.Latitude)])
    plt.figure(figsize=(12, 8))
    gdf.plot(marker='o', color='red', alpha=0.5, figsize=(12, 8))
    plt.title('Accident Hotspots in India (2014-2017)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.tight_layout()
    plt.show()

# Correlation Between Weather and Road Types
if 'Weather_Condition' in df.columns and 'Road_Type' in df.columns:
    severity_weather = df.groupby(['Weather_Condition', 'Road_Type']).size().unstack()
    plt.figure(figsize=(12, 8))
    sns.heatmap(severity_weather, annot=True, cmap='coolwarm', fmt='d', cbar_kws={'label': 'Number of Accidents'})
    plt.title('Correlation Between Weather Conditions and Road Types')
    plt.xlabel('Road Type')
    plt.ylabel('Weather Condition')
    plt.tight_layout()
    plt.show()

# Fatalities vs. Injuries Scatter Plot
if 'Fatalities' in df.columns and 'Injuries' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Fatalities', y='Injuries', hue='Year', palette='viridis', alpha=0.7, s=80)
    plt.title('Fatalities vs. Injuries by Year')
    plt.xlabel('Fatalities')
    plt.ylabel('Injuries')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Save Processed Data
output_path = r"processed_road_accidents_india_analysis.csv"
df.to_csv(output_path, index=False)
print(f"Processed data saved to {output_path}")
