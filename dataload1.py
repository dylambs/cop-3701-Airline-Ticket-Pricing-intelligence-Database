from __future__ import annotations
import csv
import os
from pathlib import Path
import oracledb


BASE_DIR = Path(__file__).resolve().parent
CSV_DIR = BASE_DIR / "csv"

oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_10")

DB_USER = "SYSTEM"
DB_PASSWORD = "YOUR_PASSWORD"
DB_DSN = "localhost:1521/XE"

def connect():
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=DB_DSN
    )


TABLE_FILES = [
    ("Airline", "Airline.csv"),
    ("City", "City.csv"),
    ("Airport", "Airport.csv"),
    ("Route", "Route.csv"),
    ("RouteLeg", "RouteLeg.csv"),
    ("Fare", "Fare.csv"),
    ("Info", "Info.csv"),
    ("FareObs", "FareObs.csv"),
]

INSERT_SQL = {
    "Airline": "INSERT INTO Airline (airline_id, airline_name) VALUES (:1, :2)",
    "City": "INSERT INTO City (city_id, city_name) VALUES (:1, :2)",
    "Airport": "INSERT INTO Airport (airport_code, city_id) VALUES (:1, :2)",
    "Route": "INSERT INTO Route (route_id, source_id, destination_id) VALUES (:1, :2, :3)",
    "RouteLeg": "INSERT INTO RouteLeg (route_id, leg_number, source_id, destination_id) VALUES (:1, :2, :3, :4)",
    "Fare": "INSERT INTO Fare (fare_id, airline_id, route_id) VALUES (:1, :2, :3)",
    "Info": "INSERT INTO Info (info_id, info_body) VALUES (:1, :2)",
    "FareObs": """
        INSERT INTO FareObs (
            obs_id, fare_id, info_id,
            journey_date, departure_time, arrival_time,
            arrival_day_offset, duration_minutes,
            total_stops, price
        )
        VALUES (
            :1, :2, :3,
            TO_DATE(:4, 'YYYY-MM-DD'),
            :5, :6,
            :7, :8,
            :9, :10
        )
    """,
}


def read_csv_rows(path: Path):
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        return list(reader)


def main():
    conn = connect()
    cur = conn.cursor()

    # clear tables safely
    delete_order = ["FareObs", "Fare", "RouteLeg", "Route", "Airport", "City", "Airline", "Info"]

    for table in delete_order:
        try:
            cur.execute(f"DELETE FROM {table}")
        except Exception:
            pass
    conn.commit()

    # load data
    for table_name, file_name in TABLE_FILES:
        rows = read_csv_rows(CSV_DIR / file_name)

        if not rows:
            print(f"Skipping {table_name} (no data)")
            continue

        cur.executemany(INSERT_SQL[table_name], rows)
        conn.commit()

        print(f"Loaded {len(rows):5} rows into {table_name}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()