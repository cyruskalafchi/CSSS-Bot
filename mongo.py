import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv

CLUSTER = os.getenv('DB_CLUSTER')
DATABASE = os.getenv('DB_NAME')
COLLECTION = os.getenv('DB_COLLECTION')

cluster = MongoClient(CLUSTER)
db = cluster[DATABASE]
collection = db[COLLECTION]

def sort_by_points():
    collection.find().sort("points")

def find_points(id):
    member = collection.find_one({'id':id})
    return member['points']

def update_points(id, points):
    attempt = collection.find_one_and_update({'id': id}, {'$inc':{'points':points}})

    if attempt == None:
        collection.insert_one({'id': id, 'points': points})

def get_top_users(range):
    sort_by_points()
    return collection.find().limit(range)


