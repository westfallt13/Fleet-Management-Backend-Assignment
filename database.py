import sqlite3

DB_PATH = "logistics.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Vehicle (
        VehicleID INTEGER PRIMARY KEY AUTOINCREMENT,
        LicensePlate TEXT NOT NULL UNIQUE,
        Model TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Driver (
        DriverID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        LicenseType TEXT NOT NULL,
        VehicleID INTEGER UNIQUE,
        FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID) ON DELETE SET NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS DeliveryRoute (
        RouteID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT NOT NULL,
        ServiceZone TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Package (
        PackageID INTEGER PRIMARY KEY AUTOINCREMENT,
        Description TEXT,
        Weight REAL,
        RouteID INTEGER,
        FOREIGN KEY (RouteID) REFERENCES DeliveryRoute(RouteID) ON DELETE SET NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS DriverRoute (
        DriverRouteID INTEGER PRIMARY KEY AUTOINCREMENT,
        DriverID INTEGER NOT NULL,
        RouteID INTEGER NOT NULL,
        Date TEXT NOT NULL,
        FOREIGN KEY (DriverID) REFERENCES Driver(DriverID) ON DELETE CASCADE,
        FOREIGN KEY (RouteID) REFERENCES DeliveryRoute(RouteID) ON DELETE CASCADE,
        UNIQUE (DriverID, RouteID, Date)
    );
    """)

    conn.commit()
    conn.close()
