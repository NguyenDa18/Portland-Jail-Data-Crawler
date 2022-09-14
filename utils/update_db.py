import pandas as pd
import os
from pymongo import MongoClient

MONGODB_CONNECTION_STRING = os.environ['MONGODB_CONNECTION_STRING']
INMATE_DETAILS_URL = "../csvs/inmate_details.csv"
INMATE_CHARGES_URL = "../csvs/inmate_charges.csv"

client = MongoClient(MONGODB_CONNECTION_STRING)

details_df = pd.read_csv(INMATE_DETAILS_URL)
charges_df = pd.read_csv(INMATE_CHARGES_URL)

# convert dataframe to dict for uploading to MongoDB
details_dict = details_df.to_dict('records')
charges_dict = charges_df.to_dict('records')

# point to mongoDB collection
db = client.data

# empty collections before inserting new inmates
db.inmates.drop()
db.inmates_charges.drop()

# insert new documents to collection
db.inmates.insert_many(details_dict)
db.inmates_charges.insert_many(charges_dict)

print("Updated MongoDB inmates data")