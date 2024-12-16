import sqlite3

# Database connection
conn = sqlite3.connect("housing.db")

# SQL query with JOIN for COVID-19 levels and aggregated metrics
query = """
SELECT 
    covid_community_level.covid_19_community_level,
    AVG(combined_data.two_bedroom) AS average_rent,
    AVG(combined_data.median_income) AS average_income,
    AVG(combined_data.covid_hospital_admissions_per_100k) AS average_hospital_admissions
FROM 
    combined_data
JOIN 
    covid_community_level 
ON 
    combined_data.covid_19_community_level_id = covid_community_level.id
WHERE 
    combined_data.two_bedroom IS NOT NULL 
    AND combined_data.median_income IS NOT NULL 
    AND combined_data.covid_hospital_admissions_per_100k IS NOT NULL
GROUP BY 
    covid_community_level.covid_19_community_level
ORDER BY 
    covid_community_level.id;
"""

# Execute the query and fetch results
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()

# Close the connection
conn.close()

# Write results to a text file
output_file = "calculated_data.txt"
with open(output_file, "w") as f:
    f.write("Metrics by COVID-19 Community Level:\n")
    f.write("COVID Level | Average Rent | Average Income | Average Hospital Admissions\n")
    f.write("-" * 65 + "\n")
    for row in rows:
        covid_level, avg_rent, avg_income, avg_hospital_admissions = row
        f.write(f"{covid_level:12} | ${avg_rent:.2f}       | ${avg_income:.2f}       | {avg_hospital_admissions:.2f} per 100k\n")

print(f"Calculated data written to {output_file}.")
