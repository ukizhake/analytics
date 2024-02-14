# Importing the FastApi class
from decimal import *
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import json
import requests

from app import app


class Item(BaseModel):
    id: int = 0 
    sourceId: str
    description: str = None
    areaInSqFt: int = 0
    fuelCombustion: str
    fuelStatus: str
    quantity: int = 0
    units: str
    category: str
    carbonEquivalent: Decimal = 0.0
    
# Default route

# A minimal app to demonstrate the get request 
@app.get("/", tags=['root'])
async def root() -> dict:
    print("ushakiz root ")
    return {"Ping": "Pong"}


# GET -- > Read Item 
@app.get("/stationaryCombustion",response_model=list) 
async def get_stationary_combustion_analytics() -> list:
    base_url = "http://35.173.120.161:8000/stationaryCombustion"
    print(" request ")
    response = requests.get(f'{base_url}')
    assert response.status_code == 200  # Validation of status code  
    rows = response.json()
    print("++++++++++++++ stat comb rows",rows, len(rows), rows[0][0])
    # Assertion of body response content:  
    assert len(rows) > 0  
    print("items "+str(rows))
    return rows


# GET -- > Read Time Series Data 
@app.get("/stationaryCombustion/timeSeries") 
async def get_stationary_combustion_timeseries_analytics()->dict:
    base_url = "http://35.173.120.161:8000/stationaryCombustion/timeSeries"
    print(" request ")
    response = requests.get(f'{base_url}')
    assert response.status_code == 200  # Validation of status code  
    rows = response.json()
    print("++++++++++++++ stat comb time series rows",rows, len(rows))
    # Assertion of body response content:  
    assert len(rows) > 0  
    print("rows "+str(rows))
    co2 = [row[0] for row in rows]
    years = [row[1] for row in rows]
    return {"years": years, "co2":co2, "rows":rows}

