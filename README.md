# Tackling-Americas-Housing-Crisis-
SI-206 Final Project Code Summary 
###
###
###
Summary of cdc.py:
The cdc.py script performs several key functions related to fetching, storing, and processing COVID-19 data.

Imports:
sqlite3: Library to interact with SQLite databases.
requests: Library to handle HTTP requests.
unittest: Library to create unit tests.

Constants:
API_URL: URL of the JSON data from the CDC.
DB_NAME: Name of the SQLite database file (housing.db).
TABLE_NAME: Name of the table to store the CDC data (er_data).

Functions:
* fetch_data(): Fetches data from the CDC API. Filters and processes the data to extract relevant columns, including county_fips, covid_hospital_admissions_per_100k, and covid_19_community_level, returning a list of tuples.
* create_tables(conn): Creates the combined_data table and covid_community_level table in the SQLite database if they don't already exist. Populates covid_community_level with predefined values ('Low', 'Medium', 'High').
* get_last_index(conn): Retrieves the count of non-null covid_hospital_admissions_per_100k entries in the combined_data table.
insert_data(conn, rows, start_index): Inserts data into the combined_data table in batches. It handles conflicts by updating existing rows based on fips_code.
* progressively_load_data(conn): Orchestrates the data loading process by fetching data, creating tables, retrieving the last index, and inserting data in batches.

Unit Testing (Commented Out):
* A test class using unittest is defined but commented out. It includes methods to test database values for specific conditions.

Main Execution Function:
* main(): Establishes a connection to the SQLite database and calls the progressively_load_data() function to load data.
The script's entry point calls main() to execute the data fetching and insertion process.

This script is designed to fetch COVID-19 data from a specified CDC API, store it in a local SQLite database, and, if necessary, update existing records to ensure data accuracy. The commented-out unit tests are intended to verify correct database values for particular conditions.
###
###
###
Summary of census.py:
The census.py script is designed to fetch, store, and process US Census data. It primarily works with SQLite to store the fetched data.

Imports:
sqlite3: Library to interact with SQLite databases.
requests: Library to handle HTTP requests.
unittest: Library to create unit tests (although not used in the current script).

Constants:
db_name: Name of the SQLite database file (housing.db).
variables: Specific Census variables to be fetched, including total population, median household income, owner and renter occupied housing units, and travel time to work.

Functions:
* api_url(year, variables): Constructs the URL for the US Census API based on the provided year and variables.
* create_table(cur, conn): Creates the combined_data table in the SQLite database if it doesn't already exist, ensuring that the necessary columns are set up.
* get_last_index(conn): Retrieves the count of non-null median_income entries in the combined_data table.
* insert_data(cur, conn, data, start_index): Inserts data into the combined_data table in batches. Handles conflicts by updating existing rows based on fips_code.
* process_api_data(year): Fetches data from the Census API for a specified year, processes the JSON response to extract relevant data, and constructs a list of tuples containing fips_code and median_income.

Main Execution Function:
* main(): Establishes a connection to the SQLite database, ensures the required table exists, retrieves the last index of inserted data, fetches new data from the Census API, and inserts it into the database.

The script is designed to periodically fetch US Census data, particularly focusing on median household income and related information, and store it in a local SQLite database. It uses a batch processing approach to handle large amounts of data efficiently.
###
###
###
Summary of data_processing.py
The data_processing.py script is designed to process data stored in a SQLite database called housing.db. It retrieves specific aggregated metrics based on COVID-19 community levels and writes the output to a text file.

Database Connection:
* Establishes a connection to the SQLite database named housing.db.

SQL Query:
Constructs a SQL query that:
* Joins the combined_data table with the covid_community_level table based on the covid_19_community_level_id.
* Selects the average values of the two-bedroom rent, median income, and COVID-19 hospital admissions per 100k population.
* Groups the results by the COVID-19 community level.
* Orders the results by the community level identifier.
* Ensures that the selected metrics are not null.

Execute Query and Fetch Results:
* Executes the constructed SQL query using the database connection.
* Fetches all the result rows from the query execution.

Close Connection:
* Closes the database connection.

Write Results to Text File:
* Opens a text file named calculated_data.txt in write mode.
* Writes a header line and column titles to the file.
* Iterates through the fetched result rows and writes the data to the file in a formatted manner.
* Specifies the data format including COVID-19 community level, average rent, average income, and average hospital admissions per 100k population.

Print Confirmation:
* Prints a confirmation message indicating that the calculated data has been written to the specified output file.

The script is intended to generate a report that summarizes key metrics (average rent, average income, and average hospital admissions) by different levels of COVID-19 community severity and save it to a text file. The output provides insights into how these metrics vary with the severity of COVID-19 in the community.
###
###
###
Summary of hud.py:
The hud.py script is designed to fetch, store, and process housing-related data from the HUD (U.S. Department of Housing and Urban Development) API, particularly focusing on rent costs for two-bedroom apartments. It operates by fetching data in batches and storing or updating this data in a local SQLite database. 

Imports:
sqlite3: Library to interact with SQLite databases.
requests: Library to handle HTTP requests.
unittest: Library to create unit tests (although not utilized in this specific script).

Constants:
DB_NAME: Name of the SQLite database file (housing.db).
TABLE_NAME: Name of the table (hud_data) for context, but the data is actually stored in combined_data.

Functions:
fetch_data(last_index):
***** Fetches data from the HUD API. It manages paginated requests by calculating the batch size based on the last index retrieved.
***** Utilizes two API endpoints: one to get the list of states and another to get the rent data for each state.
***** Processes the JSON response from the API to extract fips_code and two_bedroom rent values.
***** Returns a list of tuples containing the extracted data.
create_table(conn):
***** Ensures the combined_data table is created in the SQLite database if it doesn’t already exist, and defines the necessary columns.
get_last_index(conn):
***** Retrieves the count of non-null two_bedroom entries in the combined_data table to determine where to start inserting new data.
insert_data(conn, rows, start_index):
***** Inserts or updates the fetched data into the combined_data table in batches, handling conflicts by updating existing rows based on fips_code.
***** Logs the range of inserted rows.
progressively_load_data(conn):
***** Orchestrates the data loading process by creating the necessary table, getting the last index, fetching new data, and inserting it into the database in chunks.
***** Closes the database connection after the operation.

Main Execution Function:
* main():
*** Establishes a connection to the SQLite database and calls the progressively_load_data() function to load and store the data.

The script is designed to fetch detailed rental data from the HUD API, particularly focusing on two-bedroom apartment rents, and store this data in a local SQLite database. It manages data storage efficiently by handling updates and inserts on a per-county basis, ensuring that existing data is not duplicated.
###
###
###
Summary of visualization.py:
The visualization.py script is designed to generate various visualizations using data stored in an SQLite database (housing.db). The visualizations aim to explore relationships between housing costs, median incomes, and COVID-19 community levels. 

Imports:
* pandas for data manipulation and analysis.
* matplotlib.pyplot and seaborn for creating visualizations.
* sqlite3 for interacting with the SQLite database.

Database Connection:
* Establishes a connection to the SQLite database named housing.db.

Data Query:
* Constructs and executes an SQL query to fetch relevant data from the combined_data table. The selected data includes two_bedroom rent costs, median income, COVID-19 community level ID, and COVID-19 hospital admissions per 100k.
* Loads the queried data into a pandas DataFrame for further processing.

Close Database Connection:
* Closes the database connection after fetching the required data.

Data Processing:
* Maps COVID-19 community level IDs (covid_19_community_level_id) to descriptive labels (Low, Medium, High).
* Ensures the COVID-19 levels are treated as ordered categorical data for proper plotting.

Visualization 1: Bar Chart of Average Rent by COVID-19 Level
* Plots a bar chart showing the average 2-bedroom rental cost across different COVID-19 community levels.
* Saves the plot as average_rent_bar_chart.png.
Visualization 2: Scatter Plot of Median Income vs Rental Costs
* Creates a scatter plot to show the relationship between median income and average 2-bedroom rent, colored by COVID-19 community level.
* Saves the plot as income_vs_rent_scatter.png.
Visualization 3: COVID-19 Hospital Admissions vs Rental Costs
* Generates a scatter plot illustrating the relationship between COVID-19 hospital admissions per 100k and average 2-bedroom rent, colored by COVID-19 community level.
* Saves the plot as hospital_admissions_vs_rent.png.
Visualization 4: COVID-19 Hospital Admissions vs Median Income
* Produces a scatter plot showing the correlation between COVID-19 hospital admissions per 100k and median income, colored by COVID-19 community level.
* Saves the plot as hospital_admissions_vs_income.png.
Visualization 5: Stacked Bar Chart of Rent Ranges by COVID-19 Level
* Creates a stacked bar chart displaying the distribution of counties across different rent ranges (< $1000, $1000-$1500, etc.) within each COVID-19 community level.
* Normalizes counts to show proportions and saves the plot as stacked_bar_chart.png.

Each visualization is aimed at providing insights into how COVID-19 community levels intersect with housing and economic variables, helping to identify patterns and correlations.
