import sqlite3 
import requests
import unittest

db_name = "housing_crisis.db"
table_name = 'census_data'
batch_size = 25
variables = VARIABLES = "NAME,B01001_001E,B19013_001E,B25003_002E,B25003_003E,B08303_001E"
# B01001_001E: Total Sex by Age (Population)
# B19013_001E: MEDIAN HOUSEHOLD INCOME IN THE PAST 12 MONTHS
# B25003_002E: Owner Occupied
# B25003_003E: Renter Occupied
# B08303_001E: Travel Time to Work

def api_url(year, variables):
    return f"https://api.census.gov/data/{year}/acs/acs1?get={variables}&for=county:*"


def create_table(cur, conn):
    cur.execute(f""" 
        CREATE TABLE IF NOT EXISTS census_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            population INTEGER,
            median_income INTEGER, 
            owner_occupied INTEGER,
            renter_occupied INTEGER,
            commute_time INTEGER, 
            fips_code TEXT
        )
    """)
    conn.commit()