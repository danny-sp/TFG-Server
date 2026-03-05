from dotenv import load_dotenv
import json
import os
import requests

load_dotenv()

API_KEY = os.getenv("OCM_API_KEY")
URL = f"https://api.openchargemap.io/v3/poi/?output=json&countrycode=ES&maxresults=100000&key={API_KEY}"

print("Downloading data...")
response = requests.get(URL)

if response.status_code == 200:
    data = response.json()
    print(f"{len(data)} Charging Stations were downloaded.")

    with open('stations_data.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, indent=4, ensure_ascii=False)

else:
    print(f"Failed to download data. Status code: {response.status_code}")
