import sqlite3 
import requests
import unittest

db_name = "housing.db"
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


def get_last_index(conn):
    cur = conn.execute("SELECT MAX(id) FROM census_data;") 
    result = cur.fetchone()
    if result and result[0]:
        return result[0]
    else:
        return 0


def insert_data(cur, conn, data, start_index):
    sql = """
        INSERT INTO census_data (
            county_name,
            population,
            median_income,
            owner_occupied,
            renter_occupied,
            commute_time,
            fips_code
        ) VALUES (?,?,?,?,?,?,?); 
    """
    if start_index > 99:
        batch_size = 377
    
    end_index = start_index + batch_size
    batch_data = data[start_index:end_index]

    counter = 0
    for row in batch_data:
        conn.execute(sql, row)
        print(f'Row {counter} successfully inserted.')
        counter += 1
    conn.commit()

def process_api_data(year):
    response = requests.get(api_url(variables, year))
    if response.status_code == 200:
        data = response.json()
        headers = data[0]
        rows = data[1:]
        batch = []
        counter = 0
        for row in rows:
            fips = row[6] + row[7]
            batch.append((
                row[0],
                int(row[1]) if row[1] != None else None,
                int(row[2]) if row[2] != None else None,
                int(row[3]) if row[3] != None else None,
                int(row[4]) if row[4] != None else None, 
                int(row[5]) if row[5] != None else None,
                fips
            ))
        
        return batch
    else:
        return 'Error.'

