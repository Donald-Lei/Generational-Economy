import sqlite3
import os 
from dotenv import load_dotenv
import pandas as pd
from fredapi import Fred

load_dotenv()

FRED_API_KEY = os.environ["FRED_API_KEY"]
fred = Fred(api_key=FRED_API_KEY)

SERIES = ["UNRATE", "FEDFUNDS", "CPIAUCSL", "USREC"] 
DB_PATH = "fred_real.db"

def fetch_series(series_ids):   
    raw = {}
    for series_id in series_ids:
        raw[series_id] = fred.get_series(series_id)
    return raw

def transform(rawData):
    frames = []
    for series_id, data in rawData.items():
            df = data.reset_index()
            df.columns = ["obs_date", "value"]
            df["series_id"] = series_id
            df["obs_date"] = df["obs_date"].dt.strftime("%Y-%m-%d")
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df["value"] = df["value"].astype(object).where(df["value"].notna(), None)
            df = df.sort_values("obs_date", ascending = True)
            frames.append(df[["series_id", "obs_date", "value"]])
    return pd.concat(frames, ignore_index = True)

def load(df, db_path):
    conn = sqlite3.connect(db_path)
    df.to_sql("observations", conn, if_exists="replace", index = False)
    conn.close()
    
def main():
    rawData = fetch_series(SERIES)
    df = transform(rawData)
    load(df, DB_PATH)

if __name__ == "__main__":
    main()