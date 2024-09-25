#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:31:17 2024

@author: ayan
"""

# In[]

import pymongo
import sys
sys.path.append('.')
import pandas as pd

# In[]

# Read the TSV file using pandas
file_path = '/app/data/correct_twitter_201904.tsv'
# file_path = '/home/ayan/potato/flask_app/data/correct_twitter_201904.tsv'
data = pd.read_csv(file_path, delimiter='\t')

# Clean column names
data.columns = data.columns.str.lower()
data.columns = data.columns.str.replace('[^A-Za-z0-9]+', '_').str.strip('_')
        
# Convert 'ts1' and 'ts2' columns to datetime
if 'ts1' in data.columns:
    data['ts1'] = pd.to_datetime(data['ts1'], errors='coerce')

if 'ts2' in data.columns:
    data['ts2'] = pd.to_datetime(data['ts2'], errors='coerce')

# Convert the dataframe to a list of dictionaries for MongoDB insertion
df = data.to_dict(orient='records')


# In[]

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://mongodb:27017/')
db = client["silverspace"]
# Collection Name
col = db["twitter"]

# Clear the collection if it exists
col.delete_many({})


# Insert data into MongoDB
if df:
    col.insert_many(df)
    print(f"Inserted {len(data)} tweets into MongoDB.")
