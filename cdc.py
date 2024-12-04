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
