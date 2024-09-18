import sqlite3
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
query = "CREATE TABLE urls(url, alias, timestamp, id)"

def createTable():
    cursor.execute(query)
    db.commit
    

    

