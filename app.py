import oracledb

oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_10")

def connect():
    return oracledb.connect(
        user="SYSTEM",
        password="YOUR_PASSWORD",
        dsn="localhost:1521/XE"
    )

# =========================
# FEATURE 1
# =========================
def feature1(conn):
    cursor = conn.cursor()

    print("\nSearch Flights")
    origin = input("Enter origin airport id (this will look like three letters, 'ABC' ): ")
    destination = input("Enter destination airport id (this will look like three letters, 'ABC' ): ")

    cursor.execute("""
        SELECT fo.price,
               fo.journey_date,
               fo.departure_time,
               fo.arrival_time
        FROM FareObs fo
        JOIN Fare f ON fo.fare_id = f.fare_id
        JOIN Route r ON f.route_id = r.route_id
        WHERE r.source_id = :1
          AND r.destination_id = :2
    """, [origin, destination])

    results = cursor.fetchall()

    if not results:
        print("No flights found.")
        return

    print(f"\nFound {len(results)} flights:\n")
    for row in results:
        print(row)
def feature2(conn):
    cursor = conn.cursor()

    print("\nPrice Trends for a Route")
    route_id = input("Enter route ID: ")

    cursor.execute("""
        SELECT fo.journey_date,
               fo.price
        FROM FareObs fo
        JOIN Fare f ON fo.fare_id = f.fare_id
        WHERE f.route_id = :1
        ORDER BY fo.journey_date
    """, [route_id])

    results = cursor.fetchall()

    if not results:
        print("No price data found.")
        return

    print(f"\nPrice history for Route {route_id}:\n")
    for row in results:
        print(f"Date: {row[0]} | Price: {row[1]}")

def feature3(conn):
    cursor = conn.cursor()

    print("\nCheapest Flights by Route")

    cursor.execute("""
        SELECT r.route_id,
               a.airline_id,
               MIN(fo.price) AS cheapest_price
        FROM FareObs fo
        JOIN Fare f ON fo.fare_id = f.fare_id
        JOIN Route r ON f.route_id = r.route_id
        JOIN Airline a ON f.airline_id = a.airline_id
        GROUP BY r.route_id, a.airline_id
        ORDER BY cheapest_price
    """)

    results = cursor.fetchall()

    if not results:
        print("No data found.")
        return

    print("\nCheapest options:\n")
    for row in results:
        print(f"Route {row[0]} | Airline {row[1]} | Price: {row[2]}")
def feature4(conn):
    cursor = conn.cursor()

    print("\nAirline Performance (Average Prices)")

    cursor.execute("""
        SELECT a.airline_name,
               AVG(fo.price) AS avg_price
        FROM FareObs fo
        JOIN Fare f ON fo.fare_id = f.fare_id
        JOIN Airline a ON f.airline_id = a.airline_id
        GROUP BY a.airline_name
        ORDER BY avg_price
    """)

    results = cursor.fetchall()

    if not results:
        print("No data found.")
        return

    print("\nAirline averages:\n")
    for row in results:
        print(f"{row[0]} | Avg Price: {round(row[1], 2)}")
def feature5(conn):
    cursor = conn.cursor()

    print("\nSeasonal Price Trends")
    route_id = input("Enter route ID: ")

    cursor.execute("""
        SELECT EXTRACT(MONTH FROM fo.journey_date) AS month,
               AVG(fo.price) AS avg_price
        FROM FareObs fo
        JOIN Fare f ON fo.fare_id = f.fare_id
        WHERE f.route_id = :1
        GROUP BY EXTRACT(MONTH FROM fo.journey_date)
        ORDER BY month
    """, [route_id])

    results = cursor.fetchall()

    if not results:
        print("No seasonal data found.")
        return

    print(f"\nMonthly trends for Route {route_id}:\n")
    for row in results:
        print(f"Month: {row[0]} | Avg Price: {round(row[1], 2)}")
# ========================
# MENU
# =========================
def menu():
    print("\n--- Airline Database Menu ---")
    print("1. Search Flights")
    print("2. Price Trends")
    print("3. Cheapest Flights")
    print("4. Airline Performance")
    print("5. Seasonal Trends")
    print("6. Exit")

def main():
    conn = connect()
    cursor = conn.cursor()   # ✅ ADD THIS

    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            feature1(conn)

        elif choice == "2":
            feature2(conn)
        elif choice == "3":
            feature3(conn)
        elif choice == "4":
            feature4(conn)
        elif choice == '5':
            feature5(conn)
        elif choice == "6":
            break

        else:
            print("Feature not implemented yet")

    cursor.close()
    conn.close()
if __name__ == "__main__":
    main()