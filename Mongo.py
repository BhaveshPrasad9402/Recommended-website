from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["prime_clone"]
collection = db["my_list"]

# Load CSV data
data = pd.read_csv("amazon_prime_titles.csv")
records = data.to_dict(orient="records")

# Insert records into MongoDB
collection.insert_many(records)
print("Data imported successfully!")
