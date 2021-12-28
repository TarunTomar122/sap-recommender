from flask import Flask

from flask_pymongo import pymongo
import certifi
ca = certifi.where()


CONNECTION_STRING = "mongodb+srv://admin:admin1234@sap.05vye.mongodb.net/sap?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING, tlsCAFile=ca)

db = client.get_database('sap')
user_collection = pymongo.collection.Collection(db, 'articles')
