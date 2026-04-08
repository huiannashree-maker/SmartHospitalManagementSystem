from pymongo import MongoClient
import os

def get_mongo_connection():
    client = MongoClient("mongodb://localhost:27017/")
    return client['hospital_db']

# Note: Your hospital.db in /instance will still be used by SQLAlchemy
# for patient logins/registration if you use standard Flask-Login patterns.