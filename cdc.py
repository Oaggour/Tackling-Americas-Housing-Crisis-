import sqlite3
import requests
import unittest

# URL of the JSON data
API_URL = "https://data.cdc.gov/api/views/3nnm-4jni/rows.json?accessType=DOWNLOAD"
DB_NAME = "cdc_data.db"
TABLE_NAME = "er_data"
BATCH_SIZE = 25

def fetch_data():
    """
    Fetches data from the API URL.
    Returns:
        List of (county_fips, covid_hospital_admissions_per_100k, covid_19_community_level) tuples.
    """
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        rows = data['data']
        
        # Extract relevant columns
        extracted_data = [] 
        for row in rows:

            if row[19] == '2023-05-11T00:00:00':
                extracted_data.append((row[9], row[16], row[18]))
            
        return extracted_data
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def create_table(conn):
    """
    Creates the `er_data` table if it doesn't exist.
    Args:
        conn: SQLite connection object.
    """
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        county_fips TEXT,
        covid_hospital_admissions_per_100k REAL,
        covid_19_community_level TEXT
    );
    """
    conn.execute(create_table_sql)
    conn.commit()

def get_last_index(conn):
    """
    Gets the last index inserted in the database.
    Args:
        conn: SQLite connection object.
    Returns:
        int: Last index inserted in the database.
    """
    query_sql = f"SELECT MAX(id) FROM {TABLE_NAME};"
    cursor = conn.execute(query_sql)
    result = cursor.fetchone()
    
    if result and result[0]:
        return result[0]
    else:
        return 0

def insert_data(conn, rows, start_index):
    """
    Inserts data in batches into the database.
    Args:
        conn: SQLite connection object.
        rows: List of tuples (county_fips, covid_hospital_admissions_per_100k, covid_19_community_level).
        start_index: The starting index for insertion.
    """
    if start_index > 99:
        BATCH_SIZE = 1000
    
    end_index = start_index + BATCH_SIZE
    batch_data = rows[start_index:end_index]
    insert_sql = f"""
    INSERT INTO {TABLE_NAME} (
        county_fips,
        covid_hospital_admissions_per_100k,
        covid_19_community_level
    ) VALUES (?,?,?);
    """
    for row in batch_data:
        conn.execute(insert_sql, row)
    conn.commit()
    print(f"Inserted rows {start_index + 1} to {end_index}")


def progressively_load_data(conn):
    rows = fetch_data()
    
    if not rows:
        print("No data fetched.")
        return

    # Create table if it doesn't exist
    create_table(conn)
    
    # Get last index inserted in the database
    last_index = get_last_index(conn)
    
    # Insert data in chunks of BATCH_SIZE
    insert_data(conn, rows, last_index)
    
    # Close the database connection
    conn.close()




class Testing(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(DB_NAME)
    
    def tearDown(self):
        self.conn.close()
    
    def test_database_values(self):
        query = "SELECT * FROM er_data WHERE county_fips = ?"
        cursor = self.conn.execute(query,('05021',))
        result = cursor.fetchone()
        self.assertEqual(result[2], 1.9)

        cursor = self.conn.execute(query, ('27121',))
        result = cursor.fetchone()
        self.assertEqual(result[2],1.7)
        self.assertEqual(result[3],'Low')

        

def main():
    conn = sqlite3.connect(DB_NAME)
    
    
    

if __name__ == "__main__":
    main()
    unittest.main()

