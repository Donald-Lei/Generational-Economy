from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import pandas as pd

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://[::]:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "fred_real.db"

@app.get("/api/series")
def get_series():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT series_id FROM observations")
    series = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"series": series}

@app.get("/api/observations/{series_id}")
def get_observations(series_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT obs_date, value
        FROM observations
        WHERE series_id = ?
        ORDER BY obs_date ASC;
        """,
        (series_id.upper(),),
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code = 404, detail = f"Series '{series_id}' not found.")

    return [
        {"obs_date": row["obs_date"], "value": row["value"]}
        for row in rows
    ]