from typing import Optional, List, Dict, Any
from database import get_db_connection

# ---------- Helpers ----------

def row_to_dict(row):
    return dict(row) if row else None

    #--Driver Crud--
    
    def create_driver(name, license_type, vehicle_id=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Driver (Name, LicenseType, VehicleID) VALUES (?, ?, ?)",
        (name, license_type, vehicle_id),
    )
    conn.commit()
    driver_id = cur.lastrowid
    row = cur.execute("SELECT * FROM Driver WHERE DriverID = ?", (driver_id,)).fetchone()
    conn.close()
    return row_to_dict(row)


def get_all_drivers():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Driver").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def get_driver_by_id(driver_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM Driver WHERE DriverID = ?", (driver_id,)).fetchone()
    conn.close()
    return row_to_dict(row)


def update_driver(driver_id, name=None, license_type=None, vehicle_id=None):
    fields = []
    params = []

    if name is not None:
        fields.append("Name = ?")
        params.append(name)
    if license_type is not None:
        fields.append("LicenseType = ?")
        params.append(license_type)
    if vehicle_id is not None:
        fields.append("VehicleID = ?")
        params.append(vehicle_id)

    if not fields:
        return get_driver_by_id(driver_id)

    params.append(driver_id)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"UPDATE Driver SET {', '.join(fields)} WHERE DriverID = ?", params)
    conn.commit()
    row = cur.execute("SELECT * FROM Driver WHERE DriverID = ?", (driver_id,)).fetchone()
    conn.close()
    return row_to_dict(row)


def delete_driver(driver_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Driver WHERE DriverID = ?", (driver_id,))
    conn.commit()
    changed = cur.rowcount
    return changed > 0

#--Vehicle Crud--

def create_vehicle(license_plate, model):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Vehicle (LicensePlate, Model) VALUES (?, ?)",
        (license_plate, model),
    )
    conn.commit()
    vid = cur.lastrowid
    row = cur.execute("SELECT * FROM Vehicle WHERE VehicleID = ?", (vid,)).fetchone()
    conn.close()
    return row_to_dict(row)


def get_all_vehicles():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Vehicle").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def get_vehicle_by_id(vehicle_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM Vehicle WHERE VehicleID = ?", (vehicle_id,)).fetchone()
    conn.close()
    return row_to_dict(row)


def delete_vehicle(vehicle_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Vehicle WHERE VehicleID = ?", (vehicle_id,))
    conn.commit()
    return cur.rowcount > 0

#--Route Crud--

def create_route(date, service_zone):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO DeliveryRoute (Date, ServiceZone) VALUES (?, ?)", (date, service_zone))
    conn.commit()
    rid = cur.lastrowid
    row = cur.execute("SELECT * FROM DeliveryRoute WHERE RouteID = ?", (rid,)).fetchone()
    conn.close()
    return row_to_dict(row)


def get_all_routes():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM DeliveryRoute").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

#--Package Crud--

def create_package(description, weight, route_id=None):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Package (Description, Weight, RouteID) VALUES (?, ?, ?)",
        (description, weight, route_id),
    )
    conn.commit()
    pid = cur.lastrowid
    row = cur.execute("SELECT * FROM Package WHERE PackageID = ?", (pid,)).fetchone()
    conn.close()
    return row_to_dict(row)

#--DriverRoute Crud--

def create_driver_route(driver_id, route_id, date):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO DriverRoute (DriverID, RouteID, Date) VALUES (?, ?, ?)",
        (driver_id, route_id, date),
    )
    conn.commit()
    drid = cur.lastrowid
    row = cur.execute("SELECT * FROM DriverRoute WHERE DriverRouteID = ?", (drid,)).fetchone()
    conn.close()
    return row_to_dict(row)