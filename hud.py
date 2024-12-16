import sqlite3
import requests
import unittest

DB_NAME = "housing.db"
TABLE_NAME = "hud_data"

def fetch_data(last_index):
    """
    Fetches data from the API URL.
    Returns:
        List of (county_fips, covid_hospital_admissions_per_100k, covid_19_community_level) tuples.
    """
    BATCH_SIZE = 25
    if last_index > 99:
        BATCH_SIZE = 1000
    end_index = last_index + BATCH_SIZE
    batch = []
    url = "https://www.huduser.gov/hudapi/public/fmr/listStates"
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI2IiwianRpIjoiOGM1M2QwNTljMzhjODdjNjljMzM0OWM1M2RlN2MwM2Q0NTNjODYzYTRjMTFiMzllOGRiODE5ZDBjZTg2YjA0YWFlNjE3YTlkNWZlYzQ1NjEiLCJpYXQiOjE3MzMxNzUwOTkuOTUxNzkyLCJuYmYiOjE3MzMxNzUwOTkuOTUxNzk0LCJleHAiOjIwNDg3MDc4OTkuOTQ2MjUyLCJzdWIiOiI4MzIyMiIsInNjb3BlcyI6W119.C1ut5kUQY5UpLuui3yiHQwxroyYeQvsLt5_JHY0tLN-sK2FvbxrMoFhqkga7YMurnObI3sb3vlkQsLY8ONZxOA"}  
    response = requests.get(url, headers=headers)
    states = []
    if response.status_code == 200:
        states = response.json()
    for state in states:
        if len(batch) > end_index:
            break
        state_code = state["state_code"]
        url = f"https://www.huduser.gov/hudapi/public/fmr/statedata/{state_code}"
        headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI2IiwianRpIjoiOGM1M2QwNTljMzhjODdjNjljMzM0OWM1M2RlN2MwM2Q0NTNjODYzYTRjMTFiMzllOGRiODE5ZDBjZTg2YjA0YWFlNjE3YTlkNWZlYzQ1NjEiLCJpYXQiOjE3MzMxNzUwOTkuOTUxNzkyLCJuYmYiOjE3MzMxNzUwOTkuOTUxNzk0LCJleHAiOjIwNDg3MDc4OTkuOTQ2MjUyLCJzdWIiOiI4MzIyMiIsInNjb3BlcyI6W119.C1ut5kUQY5UpLuui3yiHQwxroyYeQvsLt5_JHY0tLN-sK2FvbxrMoFhqkga7YMurnObI3sb3vlkQsLY8ONZxOA"}  
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            rows = response.json()["data"]["counties"]
            if rows[0]["fips_code"][-5:] == "99999" and rows[-1]["fips_code"][-5:] == "99999":
                for row in rows:
                        batch.append((
                            row['town_name'],
                            row['county_name'],
                            row['metro_name'],
                            row['fips_code'][:5],
                            int(row['Efficiency']) if row['Efficiency'] != None else None,
                            int(row['One-Bedroom']) if row['One-Bedroom'] != None else None,
                            int(row['Two-Bedroom']) if row['Two-Bedroom'] != None else None,
                            int(row['Three-Bedroom']) if row['Three-Bedroom'] != None else None,
                            int(row['Four-Bedroom']) if row['Four-Bedroom'] != None else None,
                            int(row['FMR Percentile']) if row['FMR Percentile'] != None else None,
                            row['statename'],
                            row['statecode'],
                            int(row['smallarea_status']) if row['smallarea_status'] != None else None
                        ))
        else:
            print(f"Failed to fetch data: {response.status_code}")

    return batch

def create_table(conn):
    """
    Creates the `er_data` table if it doesn't exist.
    Args:
        conn: SQLite connection object.
    """
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS hud_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        town_name TEXT,
        county_name TEXT,
        metro_name TEXT,
        fips_code TEXT UNIQUE,
        Efficiency INTEGER,
        One_Bedroom INTEGER,
        Two_Bedroom INTEGER,
        Three_Bedroom INTEGER,
        Four_Bedroom INTEGER,
        FMR_Percentile INTEGER,
        statename TEXT,
        statecode TEXT,
        smallarea_status INTEGER
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
    BATCH_SIZE = 25
    if start_index > 99:
        BATCH_SIZE = 1000
    
    end_index = start_index + BATCH_SIZE
    batch_data = rows[start_index:end_index]
    insert_sql = f"""
    INSERT INTO hud_data (
        town_name,
        county_name,
        metro_name,
        fips_code,
        Efficiency,
        One_Bedroom,
        Two_Bedroom,
        Three_Bedroom,
        Four_Bedroom,
        FMR_Percentile,
        statename,
        statecode,
        smallarea_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    for row in batch_data:
        conn.execute(insert_sql, row)
    conn.commit()
    print(f"Inserted rows {start_index + 1} to {end_index}")


def progressively_load_data(conn):
    # Create table if it doesn't exist
    create_table(conn)
    
    # Get last index inserted in the database
    last_index = get_last_index(conn)


    rows = fetch_data(last_index)
    
    if not rows:
        print("No data fetched.")
        return

   
    
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
    progressively_load_data(conn)
    
    
    

if __name__ == "__main__":
    main()
    # unittest.main()
