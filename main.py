from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from typing import List
from fastapi import Query

import json
from pathlib import Path

app = FastAPI()

nav_data = []  # Global variable to store the data

@app.on_event("startup")
def load_nav_data():
    global nav_data
    with open("nav_data.json", "r") as f:
        nav_data = json.load(f)


@app.get("/")
def index():
    return {"message": "NAV API is running"}


@app.get("/nav")
def get_all_navs():
    return nav_data


@app.get("/nav/vijay")
def get_nav_vijay():

    mfs_to_filter = [
        {
            "scheme_id": "19232",
            "scheme_name": "Parag Parikh Flexi Cap FundFlexi Cap",
        },
        {
            "scheme_id": "21891",
            "scheme_name": "PGIM India Midcap Opportunities FundMid Cap",
        },
        {
            "scheme_id": "16144",
            "scheme_name": "Canara Robeco Emerging Equities FundLarge & MidCap",
        },
        {
            "scheme_id": "16126",
            "scheme_name": "Mirae Asset Large & Midcap FundLarge & MidCap",
        },
        {
            "scheme_id": "42175",
            "scheme_name": "Kotak Multicap FundMulti Cap",
        },
        {
            "scheme_id": "16925",
            "scheme_name": "Quant Small Cap FundSmall Cap",
        },
        {
            "scheme_id": "38680",
            "scheme_name": "DSP Healthcare FundSectoral-Pharma",
        },
        {
            "scheme_id": "39186",
            "scheme_name": "Tata Balanced Advantage FundDynamic Asset Allocation",
        },
        {
            "scheme_id": "15354",
            "scheme_name": "SBI Small Cap FundSmall Cap",
        },
        {
            "scheme_id": "38470",
            "scheme_name": "Tata Small Cap FundSmall Cap",
        },
        {
            "scheme_id": "39296",
            "scheme_name": "Canara Robeco Small Cap FundSmall Cap",
        },
        {
            "scheme_id": "40721",
            "scheme_name": "Motilal Oswal Nifty Smallcap 250 Index FundSmall Cap Index",
        },
        {
            "scheme_id": "44997",
            "scheme_name": "Tata Nifty Capital Markets Index FundOther Equity Index",
        },
        {
            "scheme_id": "45257",
            "scheme_name": "Motilal Oswal Innovation Opportunities FundThematic",
        }
    ]

    print(len(mfs_to_filter))
    
    ids = [scheme["scheme_id"] for scheme in mfs_to_filter]

    print(ids)


    return ids

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


@app.get("/nav/")
def get_nav_by_ids(scheme_ids: List[str] = Query(...)):
    results = [item for item in nav_data if item["scheme_id"] in scheme_ids]
    if not results:
        raise HTTPException(status_code=404, detail="No matching schemes found")
    return results