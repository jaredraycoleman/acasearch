import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
import datetime
import pathlib
import dotenv

dotenv.load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

thisdir = pathlib.Path(__file__).parent.absolute()

# Function to convert date strings to datetime objects
def convert_date(date_str):
    if pd.isnull(date_str):
        return None
    try:
        print(f"date_str: {date_str}")
        d = datetime.datetime.strptime(date_str, '%d-%b')
        # set d year to current year if date is in the past
        d = d.replace(year=datetime.datetime.now().year)
        return d
    except ValueError:
        return None

# MongoDB connection
def main():
    csv_file = thisdir / 'data.csv'
    df = pd.read_csv(csv_file)

    client = MongoClient(MONGO_URI)
    db = client.acasearch
    collection = db.conferences

    # replace nans with None
    df = df.where(pd.notnull(df), None)
    df = df.replace({np.nan: None})

    # Iterate over the DataFrame and insert each row into MongoDB
    for index, row in df.iterrows():
        conference = {
            'acronym': row['conference'],
            'h5_index': row['h5_index'] if pd.notnull(row['h5_index']) else None,
            'core_rank': row['core_rank'],
            'era_rank': row['era_rank'],
            'qualis_rank': row['qualis_rank'],
            'deadline': convert_date(row['deadline']),
            'notification_date': convert_date(row['notification']),
            'start_date': convert_date(row['start']),
            'end_date': convert_date(row['end']),
            'location': row['location'],
            'name': row['name'],
            'description': row['topics']
        }
        collection.replace_one(
            {'acronym': row['conference']},  # Query to find existing document by acronym
            conference,  # New data to replace or insert
            upsert=True  # Create a new document if no match is found
        )

    print("Conferences uploaded successfully!")

if __name__ == '__main__':
    main()