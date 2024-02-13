# Importing the FastApi class
import pymysql 

from decimal import *
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pandas as pd 
import json
from math import sqrt

from app import app, conn


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
async def get_items_stationary_combustion() -> list:
    print("ushakiz items ")
    cursor = conn.cursor()
    query = "SELECT id, sourceId, description, areaInSqFt, fuelCombustion, fuelStatus, quantity, units, category, carbonEquivalent FROM stationaryComb"
    cursor.execute(query)
    items = cursor.fetchall()
    cursor.close()
    print("items "+str(items))
    return items


# GET -- > Read Time Series Data 
@app.get("/stationaryCombustion/timeSeries") 
async def get_stationary_combustion_timeseries()->dict:
    print("ushakiz items - ")
    cursor = conn.cursor()
    query = "select CO2MetricTonnes, year from totalCO2Emissions where emissionType='StationaryCombustion' and biomass=0"
    cursor.execute(query)
    items = cursor.fetchall()
    cursor.close()
    co2 = [row[0] for row in items]
    years = [row[1] for row in items]
    #itemDF = pd.DataFrame(items, columns =['CO2MetricTonnes', 'year'])
    #grouped = itemDF.groupby("year")
    #co2 = grouped.CO2MetricTonnes
    #avg, std = co2.mean(), co2.std()
    #years = list(grouped.groups)
    #p = Figure(title="CO2 in Metric Tonnes by Year")
    #p.vbar(x=years, bottom=avg-std, top=avg+std, width=0.8,  fill_alpha=0.2, line_color=None, legend="CO2 stddev")
    #p.legend.location = "top_left"
    return {"years": years, "co2":co2, "items":items}

