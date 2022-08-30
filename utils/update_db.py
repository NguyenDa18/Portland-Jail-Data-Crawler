import pandas as pd
import os
from pymongo import MongoClient

MONGODB_CONNECTION_STRING = os.environ['MONGODB_CONNECTION_STRING']
CSV_URL = "../csvs/inmate_details.csv"

client = MongoClient(MONGODB_CONNECTION_STRING)

df = pd.read_csv(CSV_URL)

# convert dataframe to dict for uploading to MongoDB
inmates_dict = df.to_dict('records')

# point to mongoDB collection
db = client.data

# empty collection before inserting new inmates
db.inmates.drop()

# insert new documents to collection
db.inmates.insert_many(inmates_dict)