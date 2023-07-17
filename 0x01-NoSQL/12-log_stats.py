#!/usr/bin/env python3
"""
Write a Python script that provides some stats about Nginx
logs stored in MongoDB:

 * Database: logs
 * Collection: nginx
 * Display (same as the example):
   - first line: x logs where x is the number of documents in this collection
   - second line: Methods:
   - 5 lines with the number of documents with the
     method = ["GET", "POST", "PUT", "PATCH", "DELETE"] in this
     order (see example below - warning: it’s a tabulation before each line)
   - one line with the number of documents with:
     + method=GET
     + path=/status
"""
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
school_collection = client.logs.nginx

doc_num = school_collection.find().count()
num_get = school_collection.find({"method": "GET"}).count()
num_post = school_collection.find({"method": "POST"}).count()
num_put = school_collection.find({"method": "PUT"}).count()
num_patch = school_collection.find({"method": "PATCH"}).count()
num_delete = school_collection.find({"method": "DELETE"}).count()
status_check = school_collection.find({"path": "/status"}).count()

print("{} logs".format(doc_num))
print("Methods:")
print("\tmethod GET: {}".format(num_get))
print("\tmethod POST: {}".format(num_post))
print("\tmethod PUT: {}".format(num_put))
print("\tmethod PATCH: {}".format(num_patch))
print("\tmethod DELETE: {}".format(num_delete))
print("{} status check".format(status_check))
