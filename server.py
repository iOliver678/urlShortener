from fastapi import FastAPI, Request
import uvicorn
import json
from fastapi.responses import RedirectResponse

import sqlite_helpers

app= FastAPI()


@app.post("/upload")
async def jsonReturns(request: Request):
    json_body = await request.json()
    url = json_body['url']
    alias = json_body['alias']

    if(sqlite_helpers.insertUrl(url,alias)):
        return ({"url": url, "alias": alias})
        
    else:
        return ({"message": "error"})
        

@app.get("/all")
async def listAll():
    return(sqlite_helpers.showAll())

@app.get("/search/{alias}")
async def searchAlias(alias):
    url = sqlite_helpers.findUrl(alias)
    return RedirectResponse(url)

@app.post("/delete")
async def deleteUrl(alias):
    sqlite_helpers.deleteUrl(alias)
    return ({"message": "Succesfully deleted"})


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)