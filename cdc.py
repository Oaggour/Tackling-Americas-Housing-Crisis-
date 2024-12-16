import sqlite3
import requests
import unittest

# URL of the JSON data
API_URL = "https://data.cdc.gov/api/views/3nnm-4jni/rows.json?accessType=DOWNLOAD"
DB_NAME = "housing.db"
TABLE_NAME = "er_data"


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
            covid_19_community_level_id = 0
            if row[19] == '2022-02-24T00:00:00':
                if row[18] == 'Low':
                    covid_19_community_level_id = 1
                elif row[18] == 'Medium':
                    covid_19_community_level_id = 2
                elif row[18] == 'High':
                    covid_19_community_level_id = 3

                extracted_data.append((row[9], row[16], covid_19_community_level_id))
    
        return extracted_data
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def create_tables(conn):
    """
    Creates the `er_data` table if it doesn't exist.
    Args:
        conn: SQLite connection object.
    """
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS combined_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fips_code TEXT UNIQUE,
        covid_hospital_admissions_per_100k REAL,
        covid_19_community_level_id INTEGER,
        median_income INTEGER,
        two_bedroom INTEGER
    );
    """
    create_table_2 = """
        CREATE TABLE IF NOT EXISTS covid_community_level (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            covid_19_community_level TEXT UNIQUE
        )
    """
    insert_table_2 = """
        INSERT OR IGNORE INTO covid_community_level (
            covid_19_community_level
        )
        VALUES
        ('Low'),
        ('Medium'),
        ('High');
    """
    conn.execute(create_table_sql)
    conn.execute(create_table_2)
    conn.execute(insert_table_2)
    conn.commit()

def get_last_index(conn):
    cursor = conn.execute("SELECT COUNT(*) FROM combined_data WHERE covid_hospital_admissions_per_100k IS NOT NULL;")
    return cursor.fetchone()[0]

def insert_data(conn, rows, start_index):
    """
    Inserts data in batches into the database.
    Args:
        conn: SQLite connection object.
        rows: List of tuples (county_fips, covid_hospital_admissions_per_100k, covid_19_community_level).
        start_index: The starting index for insertion.
    """
    batch_size = 25
    if start_index > 99:
        batch_size = 1000
    
    end_index = start_index + batch_size
    batch_data = rows[start_index:end_index]
    for row in batch_data:
        conn.execute("""
        INSERT INTO combined_data (fips_code, covid_hospital_admissions_per_100k, covid_19_community_level_id)
        VALUES (?, ?, ?)
        ON CONFLICT(fips_code) DO UPDATE SET
            covid_hospital_admissions_per_100k=excluded.covid_hospital_admissions_per_100k,
            covid_19_community_level_id=excluded.covid_19_community_level_id;
        """, row)

    conn.commit()
    print(f"Inserted rows {start_index + 1} to {end_index}")


def progressively_load_data(conn):
    rows = fetch_data()
    
    if not rows:
        print("No data fetched.")
        return

    # Create table if it doesn't exist
    create_tables(conn)
    
    # Get last index inserted in the database
    last_index = get_last_index(conn)
    
    # Insert data in chunks of BATCH_SIZE
    insert_data(conn, rows, last_index)
    
    # Close the database connection
    conn.close()


# class Testing(unittest.TestCase):
#     def setUp(self):
#         self.conn = sqlite3.connect(DB_NAME)
    
#     def tearDown(self):
#         self.conn.close()
    
#     def test_database_values(self):
#         query = "SELECT * FROM er_data WHERE county_fips = ?"
#         cursor = self.conn.execute(query,('05021',))
#         result = cursor.fetchone()
#         self.assertEqual(result[2], 1.9)

#         cursor = self.conn.execute(query, ('27121',))
#         result = cursor.fetchone()
#         self.assertEqual(result[2],1.7)
#         self.assertEqual(result[3],1)

        

def main():
    conn = sqlite3.connect(DB_NAME)
    progressively_load_data(conn)
    
    
    

if __name__ == "__main__":
    main()
    # unittest.main()

