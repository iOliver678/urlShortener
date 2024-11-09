import json
import hash
import time
import random
import logging
import uvicorn
import sqlite_helpers as sqlite_helpers
from args import get_args
from datetime import datetime
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()
args = get_args()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Replace with your React app's origin (Vite defaults to port 5173)
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict this to 'POST' if you want
    allow_headers=["*"],  # You can restrict this to the necessary headers
)

db_file_path = args.db_file
sqlite_helpers.createTable(db_file_path)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the URL Shortener API"}

@app.post("/upload")
async def jsonReturns(request: Request):
    try:
        json_body = await request.json()
        url = json_body['url']
        alias = json_body.get('alias',None)
        
        if alias is None:
            time = datetime.now()
            alias = hash.createAlias(url, time)

        if(sqlite_helpers.insertUrl(url, alias, db_file_path)):
            return ({"url": url, "alias": alias})
        
        else:
            raise HTTPException(status_code=400)
            
    except Exception:
        logging.error('Error uploading, must insert a URL')
        raise HTTPException(status_code=400, detail="invalid input")

@app.get("/all")
async def listAll():
    try:
        print(f"reached endpoint, {db_file_path}")
        return(sqlite_helpers.showAll(db_file_path))
    except:
        logging.error(f'failed to reach {db_file_path}')
        return HTTPException(status_code=400, detail=f"could not find {db_file_path}")


@app.get("/search/{alias}")
async def searchAlias(alias):
    try:
        url = sqlite_helpers.findUrl(alias, db_file_path)
        return RedirectResponse(url)
    except:
        logging.error(f"could not find {alias}")
        return HTTPException(status_code=400, detail="could not find alias")

@app.post("/delete/{alias}")
async def deleteUrl(alias):
    try:
        sqlite_helpers.deleteUrl(alias, db_file_path)
        return ({"message": "Succesfully deleted entry"})
    except:
        logging.error(f"failed to delete {alias}")
        return HTTPException(status_code=400, detail="could not find/delete alias")

    
#do not touch
@app.post("/clear-table")
async def clearTable():
    sqlite_helpers.clearTable(db_file_path)
    return ({"message": "Succesfully cleared table"})

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
    uvicorn.run("server:app", host=args.host, port=args.port, reload=True)