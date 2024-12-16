import sqlite3

# Database connection
conn = sqlite3.connect("housing.db")

# Query to join the tables and calculate the average rental cost
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

# Execute the query and fetch all rows
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()

# Organize data into a dictionary for grouping
rent_by_covid_level = {}
for row in rows:
    average_rent, median_income, population, covid_level = row
    if covid_level not in rent_by_covid_level:
        rent_by_covid_level[covid_level] = {"total_rent": 0, "count": 0}
    rent_by_covid_level[covid_level]["total_rent"] += average_rent
    rent_by_covid_level[covid_level]["count"] += 1

# Calculate the averages
average_rent_by_covid = {
    covid_level: data["total_rent"] / data["count"]
    for covid_level, data in rent_by_covid_level.items()
}

# Write results to a text file
output_file = "calculated_data.txt"
with open(output_file, "w") as f:
    f.write("Average Rental Cost by COVID-19 Community Level:\n")
    for covid_level, avg_rent in average_rent_by_covid.items():
        f.write(f"{covid_level}: {avg_rent:.2f}\n")

print(f"Calculated data written to {output_file}")

# Close the connection
conn.close()
