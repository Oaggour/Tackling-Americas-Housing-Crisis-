import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
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
average_rent_by_covid = data.groupby('covid_19_community_level_id')['average_rent'].mean()
average_rent_by_covid.plot(kind='bar', color=['green', 'orange', 'red'], figsize=(10, 6))
plt.title("Average 2 Bedroom Rental Cost by COVID-19 Community Level")
plt.xlabel("COVID-19 Community Level")
plt.ylabel("2 Bedroom Average Rent")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("average_rent_bar_chart.png")
plt.show()

# Visualization 2: Scatter Plot of Median Income vs Rental Costs
# plt.figure(figsize=(10, 6))
# sns.scatterplot(
#     data=data,
#     x='median_income',
#     y='average_rent',
#     hue='covid_19_community_level_id',
#     palette='coolwarm'
# )
# plt.title("Median Income vs Average 2 Bedroom Rent")
# plt.xlabel("Median Income")
# plt.ylabel("Average 2 Br Rent")
# plt.legend(title="COVID-19 Level")
# plt.tight_layout()
# plt.savefig("income_vs_rent_scatter.png")
# plt.show()
