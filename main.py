from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import PlainTextResponse
from typing import List
from pydantic import BaseModel

import json
from pathlib import Path

app = FastAPI()

nav_data = {}  # Global variable to store the data

@app.on_event("startup")
def load_nav_data():
    global nav_data
    with open("nav_data.json", "r") as f:
        temp: List[dict] = json.load(f)
    
    for data in temp:
        nav_data[data["scheme_id"]] = data



@app.get("/")
def index():
    return {"message": "NAV API is running"}


@app.get("/nav")
def get_all_navs():
    return nav_data


@app.get("/nav/vijay")
def get_nav_vijay():

    vijay_mf_ids = [
        "19232",
        "21891",
        "16144",
        "16126",
        "42175",
        "16925",
        "38680",
        "39186",
        "15354",
        "38470",
        "39296",
        "40721",
        "44997",
        "45257"
    ]

    return [nav_data[_id] for _id in vijay_mf_ids if nav_data.get(_id, False)]

# nav csv format
@app.get("/nav/csv", response_class=PlainTextResponse)
def get_nav_csv():
    csv_file_path = Path("nav_data.csv")
    if not csv_file_path.exists():
        raise HTTPException(status_code=404, detail="CSV file not found")

    # Open and read the CSV file
    with open(csv_file_path, mode='r') as file:
        csv_data = file.read()

    # Return the content of the CSV file as plain text
    return csv_data


# eg: /nav/12345
@app.get("/nav/{scheme_id}")
def get_nav_by_id(scheme_id: str):
    result = nav_data.get(scheme_id)
    if not result:
        raise HTTPException(status_code=404, detail="No such scheme(mutual fund) exists")
    return result


# eg: /nav/?scheme_id=24536
@app.post("/nav/")
def get_nav_by_ids(scheme_id: str = Query(...)):
    
    if nav_data.get(scheme_id, False):
        nav_value = nav_data[scheme_id]["nav"]
        nav_value = nav_value.replace("₹", "")
        return int(nav_value)
    else:
        return "Not Found"


class NavRequest(BaseModel):
    scheme_ids: List[str]

@app.post("/nav/")
async def get_nav_post(data: NavRequest = Body(...)):
    nav_results = [nav_data[_id]["nav"] if nav_data.get(_id, False) else "Not Found" for _id in data.scheme_ids]
    navs = [n.replace("₹", "") for n in nav_results if "₹" in n]
    if not nav_results:
        raise HTTPException(status_code=404, detail="No matching schemes(mutual funds) found")
    return navs