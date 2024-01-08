from time import time
from fastapi import FastAPI, __version__
from routers.users_db import  users_db


app = FastAPI()

app.include_router(users_db.router)

@app.get("/")
async def root():
  return {'res': 'ok', 'version': __version__, "time": time()}
@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}