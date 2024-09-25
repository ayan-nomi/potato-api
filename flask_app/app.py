#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:46:02 2024

@author: ayan
"""

# In[]

from flask import Flask, request, jsonify
import pymongo 
import re
from datetime import datetime

app = Flask(__name__)

# Establish connection with MongoDB
client = pymongo.MongoClient('mongodb://mongodb:27017/')
db = client["silverspace"]
# col Name
col = db["twitter"]

# In[]

# Helper function to perform regex search for terms
def search_term(term):
    return {"text": {"$regex": re.compile(term, re.IGNORECASE)}}

@app.route('/query', methods=['POST'])
def query_tweets():
    term = request.json.get('term')

    # 1. Tweets per day
    tweets_per_day = list(col.aggregate([
        {"$match": search_term(term)},
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$ts1"}},
                    "tweet_count": {"$sum": 1}}}
    ]))
    
    # 2. Unique users
    unique_users = len(col.distinct("author_id", search_term(term)))
    
    # 3. Average likes
    avg_likes = list(col.aggregate([
        {"$match": search_term(term)},
        {"$group": {"_id": None, "average_likes": {"$avg": "$like_count"}}}
    ]))
    avg_likes_value = avg_likes[0]['average_likes'] if avg_likes else 0
    
    # 4. Place IDs
    places = col.distinct("place_id", search_term(term))
    
    # 5. Tweets by time of day
    tweets_by_hour = list(col.aggregate([
        {"$match": search_term(term)},
        {"$group": {"_id": {"$hour": "$ts1"}, "tweet_count": {"$sum": 1}}}
    ]))
    
    # 6. Most active user
    most_active_user = list(col.aggregate([
        {"$match": search_term(term)},
        {"$group": {"_id": "$author_id", "tweet_count": {"$sum": 1}}},
        {"$sort": {"tweet_count": -1}},
        {"$limit": 1}
    ]))
    
    response = {
        "1. tweets_per_day": tweets_per_day,
        "2. unique_users": unique_users,
        "3. average_likes": avg_likes_value,
        "4. places": places,
        "5. tweets_by_hour": tweets_by_hour,
        "6. most_active_user": most_active_user[0] if most_active_user else None
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
