from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
import json
import csv
from pathlib import Path

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


@app.get("/nav/{scheme_id}")
def get_nav_by_id(scheme_id: str):
    with open("nav_data.json", "r") as f:
        data = json.load(f)
    for item in data:
        if item["scheme_id"] == scheme_id:
            return item
    raise HTTPException(status_code=404, detail="Scheme not found")
