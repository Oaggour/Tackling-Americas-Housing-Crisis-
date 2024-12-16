import sqlite3

# Database connection
conn = sqlite3.connect("housing.db")

# Query to retrieve data from the combined table
query = """
SELECT 
    two_bedroom AS average_rent,
    median_income,
    covid_19_community_level_id
FROM 
    combined_data
WHERE 
    two_bedroom IS NOT NULL 
    AND median_income IS NOT NULL 
    AND covid_19_community_level_id IS NOT NULL;
"""

# Execute the query and fetch all rows
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()

# Map COVID-19 community level IDs to their labels
covid_levels = {1: "Low", 2: "Medium", 3: "High"}

# Organize data into a dictionary for grouping
rent_by_covid_level = {}
for row in rows:
    average_rent, median_income, covid_level_id = row
    covid_level = covid_levels.get(covid_level_id, "Unknown")
    if covid_level not in rent_by_covid_level:
        rent_by_covid_level[covid_level] = {"total_rent": 0, "count": 0}
    rent_by_covid_level[covid_level]["total_rent"] += average_rent
    rent_by_covid_level[covid_level]["count"] += 1

# Calculate the averages
average_rent_by_covid = {
    covid_level: data["total_rent"] / data["count"]
    for covid_level, data in rent_by_covid_level.items()
}

# Order the levels explicitly (Low, Medium, High)
ordered_levels = ["Low", "Medium", "High"]

# Write results to a text file
output_file = "calculated_data.txt"
with open(output_file, "w") as f:
    f.write("Average Rental Cost by COVID-19 Community Level:\n")
    for covid_level in ordered_levels:
        if covid_level in average_rent_by_covid:
            avg_rent = average_rent_by_covid[covid_level]
            f.write(f"{covid_level}: {avg_rent:.2f}\n")

print(f"Calculated data written to {output_file}")

# Close the connection
conn.close()
