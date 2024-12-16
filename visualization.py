import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Database connection
conn = sqlite3.connect("housing.db")

# Query the data for visualization
query = """
SELECT 
    two_bedroom AS average_rent,
    median_income,
    covid_19_community_level_id,
    covid_hospital_admissions_per_100k
FROM 
    combined_data
WHERE 
    two_bedroom IS NOT NULL 
    AND median_income IS NOT NULL 
    AND covid_19_community_level_id IS NOT NULL;
"""

# Load data into a DataFrame
data = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Map COVID-19 level IDs to labels
level_mapping = {1: "Low", 2: "Medium", 3: "High"}
data['covid_19_community_level'] = data['covid_19_community_level_id'].map(level_mapping)

# Ensure levels are ordered correctly
category_order = ["Low", "Medium", "High"]
data['covid_19_community_level'] = pd.Categorical(
    data['covid_19_community_level'], 
    categories=category_order, 
    ordered=True
)

# Visualization 1: Bar Chart of Average Rent by COVID-19 Level
average_rent_by_covid = data.groupby('covid_19_community_level')['average_rent'].mean()
average_rent_by_covid.plot(kind='bar', color=['green', 'orange', 'red'], figsize=(10, 6))
plt.title("Average 2-Bedroom Rental Cost by COVID-19 Community Level")
plt.xlabel("COVID-19 Community Level")
plt.ylabel("2-Bedroom Average Rent ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("average_rent_bar_chart.png")
plt.show()

# Visualization 2: Scatter Plot of Median Income vs Rental Costs
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=data,
    x='median_income',
    y='average_rent',
    hue='covid_19_community_level',
    palette='coolwarm',
    s=100
)
plt.title("Median Income vs Average 2-Bedroom Rent")
plt.xlabel("Median Income ($)")
plt.ylabel("2-Bedroom Average Rent ($)")
plt.legend(title="COVID-19 Level", loc='upper right')
plt.tight_layout()
plt.savefig("income_vs_rent_scatter.png")
plt.show()

# Visualization 3: COVID-19 Hospital Admissions vs Rental Costs
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=data,
    x='covid_hospital_admissions_per_100k',
    y='average_rent',
    hue='covid_19_community_level',
    palette='coolwarm',
    edgecolor='w',
    s=100,
    alpha=0.8
)
plt.title("COVID-19 Hospital Admissions vs 2-Bedroom Average Rent")
plt.xlabel("COVID-19 Hospital Admissions per 100k")
plt.ylabel("2-Bedroom Average Rent ($)")
plt.legend(title="COVID-19 Level", loc='upper right')
plt.tight_layout()
plt.savefig("hospital_admissions_vs_rent.png")
plt.show()

# Visualization 4: COVID-19 Hospital Admissions vs Median Income
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=data,
    x='covid_hospital_admissions_per_100k',
    y='median_income',
    hue='covid_19_community_level',
    palette='coolwarm',
    edgecolor='w',
    s=100,
    alpha=0.8
)
plt.title("COVID-19 Hospital Admissions vs Median Income")
plt.xlabel("COVID-19 Hospital Admissions per 100k")
plt.ylabel("Median Income ($)")
plt.legend(title="COVID-19 Level", loc='upper right')
plt.tight_layout()
plt.savefig("hospital_admissions_vs_income.png")
plt.show()

# Visualization 5: Stacked Bar Chart of Rent Ranges by COVID-19 Level
bins = [0, 1000, 1500, 2000, 2500, 3000, float('inf')]
labels = ["< $1000", "$1000-$1500", "$1500-$2000", "$2000-$2500", "$2500-$3000", "> $3000"]
data['rent_range'] = pd.cut(data['average_rent'], bins=bins, labels=labels, right=False)

# Count counties in each rent range for each COVID-19 level
rent_distribution = data.groupby(['covid_19_community_level', 'rent_range']).size().unstack(fill_value=0)

# Normalize for proportions
rent_distribution_normalized = rent_distribution.div(rent_distribution.sum(axis=1), axis=0)

# Plot stacked bar chart
rent_distribution_normalized.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
plt.title("Proportion of Counties by Rent Range and COVID-19 Level")
plt.xlabel("COVID-19 Community Level")
plt.ylabel("Proportion of Counties")
plt.xticks(rotation=0)
plt.legend(title="Rent Range", loc='upper right')
plt.tight_layout()
plt.savefig("stacked_bar_chart.png")
plt.show()
