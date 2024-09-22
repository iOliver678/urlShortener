import sqlite3
from datetime import datetime


db_file = "Database.db"
db = sqlite3.connect(db_file)
cursor = db.cursor()



def createTable():
   query = "CREATE TABLE IF NOT EXISTS urls(id INTEGER PRIMARY KEY, url TEXT, alias TEXT, timestamp TEXT)"
   cursor.execute(query)
   db.commit()

def insertUrl(url, alias):
    if(not isAliasInDatabase(alias)):
        time = datetime.now()
        query = f"""INSERT INTO urls(url, alias, timestamp) VALUES ('{url}','{alias}','{time}')"""
        cursor.execute(query)
        db.commit()
        return True
    else:
        print("Alias already exist")
        return False
    
def deleteUrl(alias):
    query = f"DELETE FROM urls WHERE alias='{alias}'"
    cursor.execute(query)
    db.commit()

def showAll():
    query = "SELECT * FROM urls"
    res = cursor.execute(query)
    listData = []
    allItems = res.fetchall()
    for row in allItems:
        holder = {"id": row[0], "url": row[1], "alias": row[2], "timestamp": row[3]}
        listData.append(holder)
    return listData
    

def findUrl(alias):
    query = f"SELECT url FROM urls WHERE alias='{alias}'"
    res = cursor.execute(query)
    item = res.fetchone()
    return item

def isAliasInDatabase(alias):
    query = f"""SELECT alias FROM urls WHERE alias='{alias}'"""""
    res = cursor.execute(query)
    if(res.fetchone() is None):
        return False
    else:
        return True





    

