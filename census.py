import sqlite3 
import requests
import unittest


db_name = "housing.db"
table_name = 'census_data'

variables = "NAME,B01001_001E,B19013_001E,B25003_002E,B25003_003E,B08303_001E"
# B01001_001E: Total Sex by Age (Population)
# B19013_001E: MEDIAN HOUSEHOLD INCOME IN THE PAST 12 MONTHS
# B25003_002E: Owner Occupied
# B25003_003E: Renter Occupied
# B08303_001E: Travel Time to Work

def api_url(year, variables):
    return f"https://api.census.gov/data/{year}/acs/acs1?get={variables}&for=county:*"


def create_table(cur, conn):
    cur.execute(f""" 
        CREATE TABLE IF NOT EXISTS combined_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fips_code TEXT UNIQUE,
            covid_hospital_admissions_per_100k REAL,
            covid_19_community_level_id INTEGER,
            median_income INTEGER,
            two_bedroom INTEGER
        );
    """)
    conn.commit()


def get_last_index(conn):
    cursor = conn.execute("SELECT COUNT(*) FROM combined_data WHERE covid_hospital_admissions_per_100k IS NOT NULL;")
    return cursor.fetchone()[0]


def insert_data(cur, conn, data, start_index):
    
    batch_size = 25

    if start_index > 99:
        batch_size = 377
    
    end_index = start_index + batch_size
    batch_data = data[start_index:end_index]

    counter = start_index
    for row in batch_data:
        conn.execute("""
        INSERT INTO combined_data (fips_code, median_income)
        VALUES (?, ?)
        ON CONFLICT(fips_code) DO UPDATE SET
            median_income=excluded.median_income;
        """, row)
        print(f'Row {counter} successfully inserted.')
        counter += 1
    conn.commit()

def process_api_data(year):
    response = requests.get(api_url(year, variables))
    if response.status_code == 200:
        data = response.json()
        headers = data[0]
        rows = data[1:]
        batch = []
        counter = 0
        for row in rows:
            fips = row[6] + row[7]
            batch.append((
                int(row[2]) if row[2] != None else None,
                fips
            ))
        
        return batch
    else:
        return 'Error.'

def main():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor() 
    create_table(cur, conn)

    last_index = get_last_index(conn)
    data = process_api_data('2023')
    insert_data(cur,conn,data,last_index)

if __name__ == "__main__":
    main()