import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Load the data from the processing script
data_file = "calculated_data.txt"
data = pd.read_csv(data_file)

# Database connection
conn = sqlite3.connect("housing.db")

# Query the same data for visualization
query = """
SELECT 
    h.Two_Bedroom AS average_rent,
    c.median_income,
    c.population,
    e.covid_19_community_level_id
FROM 
    hud_data h
JOIN 
    census_data c ON h.fips_code = c.fips_code
JOIN 
    er_data e ON h.fips_code = e.county_fips
WHERE 
    h.Two_Bedroom IS NOT NULL AND c.median_income IS NOT NULL AND e.covid_19_community_level_id IS NOT NULL;
"""

data = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Visualization 1: Bar Chart of Average Rent by COVID-19 Level
level_mapping = {1: "Low", 2: "Medium", 3: "High"}
data['covid_19_community_level'] = data['covid_19_community_level_id'].map(level_mapping)
category_order = ["Low", "Medium", "High"]
data['covid_19_community_level'] = pd.Categorical(
    data['covid_19_community_level'], 
    categories=category_order, 
    ordered=True
)
average_rent_by_covid = data.groupby('covid_19_community_level')['average_rent'].mean()
average_rent_by_covid.plot(kind='bar', color=['green', 'orange', 'red'], figsize=(10, 6))
plt.title("Average 2 Bedroom Rental Cost by COVID-19 Community Level")
plt.xlabel("COVID-19 Community Level")
plt.ylabel("2 Bedroom Average Rent")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("average_rent_bar_chart.png")
plt.show()

# Visualization 2: Scatter Plot of Median Income vs Rental Costs
plt.figure(figsize=(10, 6))
data['covid_19_community_level'] = data['covid_19_community_level_id'].map(level_mapping)
category_order = ["Low", "Medium", "High"]
data['covid_19_community_level'] = pd.Categorical(
    data['covid_19_community_level'], 
    categories=category_order, 
    ordered=True
)
sns.scatterplot(
    data=data,
    x='median_income',
    y='average_rent',
    hue='covid_19_community_level',
    palette='coolwarm'
)
plt.title("Median Income vs Average 2 Bedroom Rent")
plt.xlabel("Median Income")
plt.ylabel("Average 2 Br Rent")
plt.legend(title="COVID-19 Level")
plt.tight_layout()
plt.savefig("income_vs_rent_scatter.png")
plt.show()

conn = sqlite3.connect("housing.db")

query = """
SELECT 
    e.covid_hospital_admissions_per_100k,
    h.Two_Bedroom AS average_rent,
    e.covid_19_community_level_id
FROM 
    er_data e
JOIN 
    hud_data h ON e.county_fips = h.fips_code
WHERE 
    e.covid_hospital_admissions_per_100k IS NOT NULL AND h.Two_Bedroom IS NOT NULL;
"""

# Load data into a DataFrame
data = pd.read_sql_query(query, conn)


# Close connection
conn.close()

# Map numeric COVID-19 level IDs to labels
level_mapping = {1: "Low", 2: "Medium", 3: "High"}
data['covid_19_community_level'] = data['covid_19_community_level_id'].map(level_mapping)

# Ensure the levels are ordered as Low, Medium, High
category_order = ["Low", "Medium", "High"]
data['covid_19_community_level'] = pd.Categorical(
    data['covid_19_community_level'], 
    categories=category_order, 
    ordered=True
)

# Create the scatter plot
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

# Customize the plot
plt.title("COVID-19 Hospital Admissions vs 2-Bedroom Average Rent", fontsize=16)
plt.xlabel("COVID-19 Hospital Admissions per 100k", fontsize=14)
plt.ylabel("2-Bedroom Average Rent ($)", fontsize=14)
plt.legend(title="COVID-19 Level", fontsize=10, title_fontsize=12, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)

# Save and display the plot
plt.tight_layout()
plt.savefig("hospital_admissions_vs_rent.png")
plt.show()

conn = sqlite3.connect("housing.db")

query = """
SELECT 
    e.covid_hospital_admissions_per_100k,
    c.median_income,
    e.covid_19_community_level_id
FROM 
    er_data e
JOIN 
    census_data c ON e.county_fips = c.fips_code
WHERE 
    e.covid_hospital_admissions_per_100k IS NOT NULL AND c.median_income IS NOT NULL;
"""

# Load data into a DataFrame
data = pd.read_sql_query(query, conn)


# Close connection
conn.close()

# Map numeric COVID-19 level IDs to labels
level_mapping = {1: "Low", 2: "Medium", 3: "High"}
data['covid_19_community_level'] = data['covid_19_community_level_id'].map(level_mapping)

# Ensure the levels are ordered as Low, Medium, High
category_order = ["Low", "Medium", "High"]
data['covid_19_community_level'] = pd.Categorical(
    data['covid_19_community_level'], 
    categories=category_order, 
    ordered=True
)

# Create the scatter plot
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

# Customize the plot
plt.title("COVID-19 Hospital Admissions vs Median Income", fontsize=16)
plt.xlabel("COVID-19 Hospital Admissions per 100k", fontsize=14)
plt.ylabel("Median Income ($)", fontsize=14)
plt.legend(title="COVID-19 Level", fontsize=10, title_fontsize=12, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)

# Save and display the plot
plt.tight_layout()
plt.savefig("hospital_admissions_vs_income.png")
plt.show()




# Database connection
conn = sqlite3.connect("housing.db")

# Query the data
query = """
SELECT 
    h.Two_Bedroom AS average_rent,
    e.covid_19_community_level_id
FROM 
    hud_data h
JOIN 
    er_data e ON h.fips_code = e.county_fips
WHERE 
    h.Two_Bedroom IS NOT NULL AND e.covid_19_community_level_id IS NOT NULL;
"""

# Load data into a DataFrame
data = pd.read_sql_query(query, conn)


# Create rental cost ranges
bins = [0, 1000, 1500, 2000, 2500, 3000, float('inf')]
labels = ["< $1000", "$1000-$1500", "$1500-$2000", "$2000-$2500", "$2500-$3000", "> $3000"]
data['rent_range'] = pd.cut(data['average_rent'], bins=bins, labels=labels, right=False)
level_mapping = {1: "Low", 2: "Medium", 3: "High"}
data['covid_19_community_level'] = data['covid_19_community_level_id'].map(level_mapping)
category_order = ["Low", "Medium", "High"]
data['covid_19_community_level'] = pd.Categorical(
    data['covid_19_community_level'], 
    categories=category_order, 
    ordered=True
)
# Count counties in each range for each COVID-19 level
rent_distribution = data.groupby(['covid_19_community_level', 'rent_range']).size().unstack(fill_value=0)

# Normalize to show proportions
rent_distribution_normalized = rent_distribution.div(rent_distribution.sum(axis=1), axis=0)

# Plot stacked bar chart
rent_distribution_normalized.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')

# Customize the plot
plt.title("Proportion of Counties by Rent Range and COVID-19 Level", fontsize=16)
plt.xlabel("COVID-19 Community Level", fontsize=14)
plt.ylabel("Proportion of Counties", fontsize=14)
plt.xticks(rotation=0, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title="Rent Range", fontsize=10, title_fontsize=12, loc='upper right')

# Save the plot
plt.tight_layout()
plt.savefig("stacked_bar_chart.png")
plt.show()