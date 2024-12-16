import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("housing.db")

# Query to join the tables and calculate the average rental cost
query = """
SELECT 
    h.county_name,
    h.Two_Bedroom AS average_rent,
    c.median_income,
    c.population,
    e.covid_19_community_level
FROM 
    hud_data h
JOIN 
    census_data c ON h.fips_code = c.fips_code
JOIN 
    er_data e ON h.fips_code = e.county_fips
WHERE 
    h.Two_Bedroom IS NOT NULL AND c.median_income IS NOT NULL AND e.covid_19_community_level IS NOT NULL;
"""

# Load data into a pandas DataFrame
data = pd.read_sql_query(query, conn)

# Calculate averages for each COVID-19 level
average_rent_by_covid = data.groupby('covid_19_community_level')['average_rent'].mean()

# Write results to a text file
output_file = "calculated_data.txt"
with open(output_file, "w") as f:
    f.write("Average Rental Cost by COVID-19 Community Level:\n")
    f.write(average_rent_by_covid.to_string())

print(f"Calculated data written to {output_file}")

# Close the connection
conn.close()
