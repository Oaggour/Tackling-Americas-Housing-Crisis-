import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Database connection
conn = sqlite3.connect("cdc_data.db")

# Query the data
query = """
SELECT 
    h.county_name,
    h.Two_Bedroom AS average_rent,
    e.covid_19_community_level
FROM 
    hud_data h
JOIN 
    er_data e ON h.fips_code = e.county_fips
WHERE 
    h.Two_Bedroom IS NOT NULL AND e.covid_19_community_level IS NOT NULL;
"""

# Load data into a DataFrame
data = pd.read_sql_query(query, conn)

# Close connection
conn.close()

# Create rental cost ranges
bins = [0, 1000, 1500, 2000, 2500, 3000, float('inf')]
labels = ["< $1000", "$1000-$1500", "$1500-$2000", "$2000-$2500", "$2500-$3000", "> $3000"]
data['rent_range'] = pd.cut(data['average_rent'], bins=bins, labels=labels, right=False)

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
