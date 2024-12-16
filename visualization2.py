import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import seaborn as sns

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


# Query to get the data
query = """
SELECT 
    c.owner_occupied,
    h.Two_Bedroom AS average_rent,
    e.covid_19_community_level_id
FROM 
    census_data c
JOIN 
    hud_data h ON c.fips_code = h.fips_code
JOIN 
    er_data e ON c.fips_code = e.county_fips
WHERE 
    c.owner_occupied IS NOT NULL AND h.Two_Bedroom IS NOT NULL AND e.covid_19_community_level_id IS NOT NULL;
"""

# Load data into a pandas DataFrame
data = pd.read_sql_query(query, conn)


# Visualization: Scatter Plot
data['covid_19_community_level'] = data['covid_19_community_level_id'].map(level_mapping)
category_order = ["Low", "Medium", "High"]
data['covid_19_community_level'] = pd.Categorical(
    data['covid_19_community_level'], 
    categories=category_order, 
    ordered=True
)
plt.figure(figsize=(12, 8))
sns.scatterplot(
    data=data,
    x='owner_occupied',
    y='average_rent',
    hue='covid_19_community_level',
    palette='viridis',
    alpha=0.8,
    edgecolor='w',
    s=100
)

# Customize the plot
plt.title("Owner-Occupied Households vs Average Rental Costs", fontsize=16)
plt.xlabel("Owner-Occupied Households", fontsize=14)
plt.ylabel("Average Rental Cost (Two-Bedroom)", fontsize=14)
plt.legend(title="COVID-19 Level", fontsize=10, title_fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Save the plot
plt.tight_layout()
plt.savefig("owner_vs_rental_costs_scatter.png")
plt.show()

query = """
SELECT 
    h.Two_Bedroom AS average_rent,
    c.median_income,
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

# Load data into a DataFrame
data = pd.read_sql_query(query, conn)


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
    x='median_income',
    y='average_rent',
    hue='covid_19_community_level',
    palette='coolwarm',
    edgecolor='w',
    s=100,
    alpha=0.8
)

# Customize the plot
plt.title("Median Income vs 2-Bedroom Average Rent", fontsize=16)
plt.xlabel("Median Income ($)", fontsize=14)
plt.ylabel("2-Bedroom Average Rent ($)", fontsize=14)
plt.legend(title="COVID-19 Level", fontsize=10, title_fontsize=12, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)

# Save and display the plot
plt.tight_layout()
plt.savefig("median_income_vs_rent.png")
plt.show()


query = """
SELECT 
    c.renter_occupied,
    e.covid_19_community_level_id
FROM 
    census_data c
JOIN 
    er_data e ON c.fips_code = e.county_fips
WHERE 
    c.renter_occupied IS NOT NULL AND e.covid_19_community_level_id IS NOT NULL;
"""

# Load data into a DataFrame
data = pd.read_sql_query(query, conn)


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

# Group by COVID-19 levels and calculate total renter-occupied households
renter_occupied_by_covid = data.groupby('covid_19_community_level')['renter_occupied'].sum()

# Plot the bar chart
plt.figure(figsize=(10, 6))
renter_occupied_by_covid.plot(kind='bar', color=['green', 'orange', 'red'])

# Customize the plot
plt.title("Total Renter-Occupied Households by COVID-19 Community Level", fontsize=16)
plt.xlabel("COVID-19 Community Level", fontsize=14)
plt.ylabel("Total Renter-Occupied Households", fontsize=14)
plt.xticks(rotation=0)
plt.tight_layout()

# Save and display the plot
plt.savefig("renter_occupied_by_covid_level.png")
plt.show()


query = """
SELECT 
    c.commute_time,
    h.Two_Bedroom AS average_rent,
    e.covid_19_community_level_id
FROM 
    census_data c
JOIN 
    hud_data h ON c.fips_code = h.fips_code
JOIN 
    er_data e ON c.fips_code = e.county_fips
WHERE 
    c.commute_time IS NOT NULL AND h.Two_Bedroom IS NOT NULL AND e.covid_19_community_level_id IS NOT NULL;
"""

# Load data into a DataFrame
data = pd.read_sql_query(query, conn)


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
    x='commute_time',
    y='average_rent',
    hue='covid_19_community_level',
    palette='coolwarm',
    edgecolor='w',
    s=100,
    alpha=0.8
)

# Customize the plot
plt.title("Commute Time vs 2-Bedroom Average Rent", fontsize=16)
plt.xlabel("Average Commute Time (minutes)", fontsize=14)
plt.ylabel("2-Bedroom Average Rent ($)", fontsize=14)
plt.legend(title="COVID-19 Level", fontsize=10, title_fontsize=12, loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)

# Save and display the plot
plt.tight_layout()
plt.savefig("commute_time_vs_rent.png")
plt.show()

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


# Close connection
conn.close()