from fastapi import FastAPI, HTTPException
import pandas as pd
import json

app = FastAPI()

@app.get("/")
def index():
    return {"message": "NAV API is running"}

@app.get("/nav")
def get_all_navs():
    with open("nav_data.json", "r") as f:
        data = json.load(f)
    return data

# nav csv format
@app.get("/nav/csv")
def get_nav_csv():
    with open("nav_data.csv", "r") as f:
        data = f.read()
    
    # print(data)
    return data

@app.get("/nav/{scheme_id}")
def get_nav_by_id(scheme_id: str):
    with open("nav_data.json", "r") as f:
        data = json.load(f)
    for item in data:
        if item["scheme_id"] == scheme_id:
            return item
    raise HTTPException(status_code=404, detail="Scheme not found")
