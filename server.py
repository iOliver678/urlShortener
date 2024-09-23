import json
import hash
import time
import random
import logging
import uvicorn
import sqlite_helpers
from args import get_args
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app= FastAPI()
args = get_args()

db_file_path = args.db_file


@app.post("/upload")
async def jsonReturns(request: Request, db_file_path):
    json_body = await request.json()
    url = json_body['url']
    alias = json_body.get('alias',None)
    
    if alias is None:
        time = datetime.now()
        alias = hash.createAlias(url, time)

    if(sqlite_helpers.insertUrl(url, alias, db_file_path)):
        return ({"url": url, "alias": alias})
        
    else:
        return ({"message": "error"})
        

@app.get("/all")
async def listAll(db_file_path):
    return(sqlite_helpers.showAll(db_file_path))

@app.get("/search/{alias}")
async def searchAlias(alias,db_file_path):
    url = sqlite_helpers.findUrl(alias,db_file_path)
    return RedirectResponse(url)

@app.post("/delete/{alias}")
async def deleteUrl(alias,db_file_path):
    sqlite_helpers.deleteUrl(alias,db_file_path)
    return ({"message": "Succesfully deleted entry"})

@app.get("/logging-levels")
def logging_levels():
    logging.error("error message")
    logging.warning("warning message")
    logging.info("info message")
    logging.debug("debug message")


logging.Formatter.converter = time.gmtime
logging.basicConfig(
    format="%(asctime)s.%(msecs)03dZ %(levelname)s:%(name)s:%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level= logging.ERROR - (args.verbose*10),
)

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)