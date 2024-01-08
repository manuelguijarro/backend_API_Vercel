import os
from time import time
from fastapi import FastAPI, __version__
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
PORT = os.getenv("PORT")


@app.get("/")
async def root():
  return {'res': 'ok', 'version': __version__, "time": time()}
@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}