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


if __name__ == "main":
  from pymongo import MongoClient


  client = MongoClient('mongodb://127.0.0.1:27017')
  nginx = client.logs.nginx

  doc_num = nginx.count_documents({})
  num_get = nginx.count_documents({"method": "GET"})
  num_post = nginx.count_documents({"method": "POST"})
  num_put = nginx.count_documents({"method": "PUT"})
  num_patch = nginx.count_documents({"method": "PATCH"})
  num_delete = nginx.count_documents({"method": "DELETE"})
  status_check = nginx.count_documents({"path": "/status"})

  print("{} logs".format(doc_num))
  print("Methods:")
  print("\tmethod GET: {}".format(num_get))
  print("\tmethod POST: {}".format(num_post))
  print("\tmethod PUT: {}".format(num_put))
  print("\tmethod PATCH: {}".format(num_patch))
  print("\tmethod DELETE: {}".format(num_delete))
  print("{} status check".format(status_check))
