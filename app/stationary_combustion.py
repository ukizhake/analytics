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

# Route to read an item
@app.get("/stationaryCombustion/item/{id}", response_model=Item)
def get_item_stationary_combustion(id: int):
    cursor = conn.cursor()
    query = "SELECT id, sourceId, description, areaInSqFt, fuelCombustion, fuelStatus, quantity, units, category, carbonEquivalent FROM stationaryComb WHERE id=%s"
    cursor.execute(query, (id,))
    item = cursor.fetchone()
    print("item is "+str(item))
    cursor.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    print("item is "+str(item))

    # return item
    return {"id": item[0], "sourceId": item[1], "description": item[2], "areaInSqFt":item[3],  "fuelCombustion": item[4], "fuelStatus": item[5], "quantity": item[6], "units": item[7], "category": item[8], "carbonEquivalent": item[9]}

# Post -- > Create Ite5
@app.post("/stationaryCombustion/item", response_model=Item)
def create_item(item: Item):
    print("helloooo ")
    print("item is "+str(item))
    cursor = conn.cursor()
    query = "INSERT INTO stationaryComb (sourceId, description, areaInSqFt, fuelCombustion, fuelStatus, quantity, units, category, carbonEquivalent) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)"
    cursor.execute(query, (item.sourceId, item.description, item.areaInSqFt, item.fuelCombustion, item.fuelStatus, item.quantity, item.units, item.category, item.carbonEquivalent))
    print("q is "+query)
    conn.commit()
    # item.id = cursor.lastrowid
    print("item id is "+str(cursor.lastrowid))
    cursor.close()
    return item

# PUT  -- > Update Item
@app.put("/stationaryCombustion/item/{id}", response_model=Item)
async def update_item(id: int, item: Item):
    cursor = conn.cursor()
    print("update item is "+str(item))
    query = "UPDATE stationaryComb SET  sourceId=%s, description=%s, areaInSqFt=%s, fuelCombustion=%s, fuelStatus=%s, quantity=%s, units=%s, category=%s, carbonEquivalent=%s WHERE id=%s"
    cursor.execute(query, (item.sourceId, item.description, item.areaInSqFt, item.fuelCombustion, item.fuelStatus, item.quantity, item.units, item.category, item.carbonEquivalent, item.id))
    print("item is "+str(query))
    cursor.close()
    conn.commit()
    return {"id": item.id, "sourceId": item.sourceId, "description": item.description, "areaInSqFt":item.areaInSqFt,  "fuelCombustion": item.fuelCombustion, "fuelStatus": item.fuelStatus, "quantity": item.quantity, "units": item.units, "category": item.category, "carbonEquivalent": item.carbonEquivalent}


# DELETE --> Delete item 
@app.delete("/stationaryCombustion/item/{id}", response_model=dict)
def delete_item_stationary_combustion(id: int):
    cursor = conn.cursor()
    query = "DELETE FROM stationaryComb WHERE id=%s"
    res = cursor.execute(query, (id,))
    print("res "+str(res))
    conn.commit()
    cursor.close()
    if (res == 1):
        return {"result": "true"}
    else: 
        return {"result": "false"}

