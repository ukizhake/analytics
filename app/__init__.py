from fastapi import FastAPI, HTTPException
from decimal import *
import pymysql  
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://192.168.1.90:19006",
    "http://localhost:19006/",
    "http://localhost:19006",
    "*"
]
db_config = {
    'host': 'wanteetproductiondb.cb5dueds9nkn.us-east-1.rds.amazonaws.com',
    'user': 'root',
    'passwd': 'MoreT1m3',
    'db': 'ghgreport',
}
conn = pymysql.connect(**db_config)
# Creating an app object
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
