import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv

DATABASE = os.getenv('DB_NAME')
CLUSTER = os.getenv('DB_CLUSTER')
MEMBER_COLLECTION = os.getenv('DB_MEMBERS')
ROLE_COLLECTION = os.getenv('DB_ROLES')

cluster = MongoClient(CLUSTER)
db = cluster[DATABASE]
member_collection = db[MEMBER_COLLECTION]
role_collection = db[ROLE_COLLECTION]

def sort_by_points():
    return member_collection.find().sort("points", pymongo.DESCENDING)

def find_points(id):
    member = member_collection.find_one({'id': id})
    return member['points']

def update_points(id, points):
    attempt = member_collection.find_one_and_update({'id': id}, {'$inc':{'points': points}})

    if attempt == None:
        member_collection.insert_one({'id': id, 'points': points})

def get_top_users(range):
    return sort_by_points().limit(range)

def reactable_message(id):
    return role_collection.find_one({'id': id})

def delete_react_role(entry):
    role_collection.delete_one(entry)
