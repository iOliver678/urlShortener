import sqlite3
from datetime import datetime
#function for table creation
    #table will have url, alias, timestamp, id
#function for inserting a url into the table
#function for deleting a url
#function for listing all urls
#function for retrieving 1 url based on alias
#function for checking if alias exists in the db
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
    allItems = res.fetchall()
    return allItems
    

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


   
    

    

