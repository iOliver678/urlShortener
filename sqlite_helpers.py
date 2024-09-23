import sqlite3
from datetime import datetime
import hash


def createTable(db_file):
   db = sqlite3.connect(db_file)
   cursor = db.cursor()
   query = "CREATE TABLE IF NOT EXISTS urls(id INTEGER PRIMARY KEY, url TEXT, alias TEXT, timestamp TEXT)"
   cursor.execute(query)
   db.commit()

def insertUrl(url, alias, db_file):
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    if(not isAliasInDatabase(alias)):
        time = datetime.now()
        query = f"""INSERT INTO urls(url, alias, timestamp) VALUES ('{url}','{alias}','{time}')"""
        cursor.execute(query)
        db.commit()
        return True
    else:
        print("Alias already exist")
        return False
    

def deleteUrl(alias, db_file):
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    query = f"DELETE FROM urls WHERE alias='{alias}'"
    cursor.execute(query)
    db.commit()

def showAll(db_file):
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    query = "SELECT * FROM urls"
    res = cursor.execute(query)
    listData = []
    allItems = res.fetchall()
    for row in allItems:
        holder = {"id": row[0], "url": row[1], "alias": row[2], "timestamp": row[3]}
        listData.append(holder)
    return listData
    

def findUrl(alias, db_file):
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    query = f"SELECT url FROM urls WHERE alias='{alias}'"
    res = cursor.execute(query)
    item = res.fetchone()[0]
    return item

def isAliasInDatabase(alias, db_file):
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    query = f"""SELECT alias FROM urls WHERE alias='{alias}'"""""
    res = cursor.execute(query)
    if(res.fetchone() is None):
        return False
    else:
        return True
    

def clearTable(db_file):
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    query = "DELETE FROM urls"
    cursor.execute(query)
    db.commit()