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


def log_stats(nginx):
    """
    function that provides some stats about Nginx logs stored in MongoDB:
    """
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    doc_num = nginx.count_documents({})
    status_check = nginx.count_documents({"path": "/status", "method": "GET"})

    print("{} logs".format(doc_num))
    print("Methods:")
    for item in method:
        count = nginx.count_documents({"method": item})
        print("\tmethod {}: {}".format(item, count))
    print("{} status check".format(status_check))


if __name__ == "main":
    client = MongoClient('mongodb://127.0.0.1:27017')
    log_stats(client.logs.nginx)
