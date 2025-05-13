# scrape_nav.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

options.binary_location = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(options=options)
driver.get("https://www.etmoney.com/mutual-funds/filter/latest-mutual-fund-nav")
time.sleep(6)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

data = []
for row in soup.select("tr.mfFund-nav-row"):
    try:
        scheme_id = row.get("data-scheme-id")
        tds = row.find_all("td")
        scheme_name = tds[0].get_text(strip=True).replace("Invest", "")
        duration = tds[1].text.strip()
        nav = tds[2].text.strip()
        change = tds[3].text.strip()
        date = tds[4].text.strip()

        data.append({
            "scheme_id": scheme_id,
            "scheme_name": scheme_name,
            "duration": duration,
            "nav": nav,
            "change": change,
            "date": date
        })
    except Exception as e:
        print(f"Error: {e}")

with open("nav_data.json", "w") as f:
    json.dump(data, f, indent=2)

# json to csv
import pandas as pd
df = pd.read_json("nav_data.json")
df.to_csv("nav_data.csv", index=False)
