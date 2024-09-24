import json
import Backend.hash as hash
import time
import random
import logging
import uvicorn
import Backend.sqlite_helpers as sqlite_helpers
from Backend.args import get_args
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app= FastAPI()
args = get_args()

db_file_path = args.db_file
sqlite_helpers.createTable(db_file_path)


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
            return ({"message": "error"})
    except:
        logging.error('Error uploading, must insert a URL')
        return ({"message": "must upload a URL"})
        

@app.get("/all")
async def listAll():
    try:
        print(f"reached endpoint, {db_file_path}")
        return(sqlite_helpers.showAll(db_file_path))
    except:
        logging.error(f'failed to reach {db_file_path}')
        return ({"message": f"failed to retrive all from {db_file_path}"})

@app.get("/search/{alias}")
async def searchAlias(alias):
    try:
        url = sqlite_helpers.findUrl(alias, db_file_path)
        return RedirectResponse(url)
    except:
        logging.error(f"could not find {alias}")
        return ({"message": f"could not find {alias}"})

@app.post("/delete/{alias}")
async def deleteUrl(alias):
    try:
        sqlite_helpers.deleteUrl(alias, db_file_path)
        return ({"message": "Succesfully deleted entry"})
    except:
        logging.error(f"failed to delete {alias}")
        return ({"message": f"failed to delete/locate {alias}"})


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