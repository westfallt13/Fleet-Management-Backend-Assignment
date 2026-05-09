from typing import Optional, List, Dict, Any  # Import typing modules for future-proofing or code readability
from database import get_db_connection  # Import the function to retrieve a database connection instance

# ---------- Helpers ----------

def row_to_dict(row):  # Helper function mapping SQLite Row objects to standard Python dictionaries
    return dict(row) if row else None  # Return dictionary interpretation of row or None if empty

# --Driver Crud--

def create_driver(name, license_type, vehicle_id=None):  # Create a new driver 
    conn = get_db_connection()  # Connect to local DB
    cur = conn.cursor()  # Grab connection cursor object
    cur.execute(  # Execute query directly
        "INSERT INTO Driver (Name, LicenseType, VehicleID) VALUES (?, ?, ?)",  # Bind params internally
        (name, license_type, vehicle_id),  # Param list
    )
    conn.commit()  # Commit insert
    driver_id = cur.lastrowid  # Fetch newly inserted DriverID
    row = cur.execute("SELECT * FROM Driver WHERE DriverID = ?", (driver_id,)).fetchone()  # Read DB again
    conn.close()  # Cleanup DB 
    return row_to_dict(row)  # Format and return



def get_all_drivers():  # Returns all driver elements 
    conn = get_db_connection()  # Initialize connection
    rows = conn.execute("SELECT * FROM Driver").fetchall()  # SQL script retrieving all drivers
    conn.close()  # Shut door
    return [row_to_dict(r) for r in rows]  # Mapping iterable rows to Python dicts


def get_driver_by_id(driver_id):  # Fetch specific driver from DB
    conn = get_db_connection()  # Make connection
    row = conn.execute("SELECT * FROM Driver WHERE DriverID = ?", (driver_id,)).fetchone()  # Filter by primary key
    conn.close()  # Done querying
    return row_to_dict(row)  # Return single element


def update_driver(driver_id, name=None, license_type=None, vehicle_id=None):  # Allow patching driver rows
    fields = []  # SQL strings to update
    params = []  # Parameter binding container

    if name is not None:  # Optional block: Name
        fields.append("Name = ?")  # String modifier
        params.append(name)  # Assign to var array
    if license_type is not None:  # Optional block: License
        fields.append("LicenseType = ?")  # String modifier
        params.append(license_type)  # Assign to var array
    if vehicle_id is not None:  # Optional block: Vehicle foreign key referencing
        fields.append("VehicleID = ?")  # String modifier
        params.append(vehicle_id)  # Assign to var array

    if not fields:  # Guard preventing crash if missing vars
        return get_driver_by_id(driver_id)  # Returns unchanged item

    params.append(driver_id)  # Attach where condition reference argument 

    conn = get_db_connection()  # Request connection
    cur = conn.cursor()  # Active context object
    cur.execute(f"UPDATE Driver SET {', '.join(fields)} WHERE DriverID = ?", params)  # F-string executing SQL build
    conn.commit()  # Commit results
    row = cur.execute("SELECT * FROM Driver WHERE DriverID = ?", (driver_id,)).fetchone()  # Return modified
    conn.close()  # End database flow
    return row_to_dict(row)  # Final serialization


def delete_driver(driver_id):  # Removes a driver
    conn = get_db_connection()  # Query connection
    cur = conn.cursor()  # Context setup
    cur.execute("DELETE FROM Driver WHERE DriverID = ?", (driver_id,))  # Drop statement
    conn.commit()  # Commit changes internally
    changed = cur.rowcount  # Validate rows dropped
    return changed > 0  # Yield bool status

#--Vehicle Crud--

def create_vehicle(license_plate, model):  # Initializes generic vehicle object
    conn = get_db_connection()  # Spin up DB connection
    cur = conn.cursor()  # Open db context
    cur.execute(  # Standard insert workflow
        "INSERT INTO Vehicle (LicensePlate, Model) VALUES (?, ?)",  # Using parameter safety
        (license_plate, model),  # Safe value assignment
    )
    conn.commit()  # Lock change 
    vid = cur.lastrowid  # VehicleID lookup
    row = cur.execute("SELECT * FROM Vehicle WHERE VehicleID = ?", (vid,)).fetchone()  # Select confirmation
    conn.close()  # Disconnect instance
    return row_to_dict(row)  # Formatting


def get_all_vehicles():  # Gets every vehicle inside DB
    conn = get_db_connection()  # Ready DB API
    rows = conn.execute("SELECT * FROM Vehicle").fetchall()  # Get array 
    conn.close()  # Free memory limit
    return [row_to_dict(r) for r in rows]  # JSON serializable data


def get_vehicle_by_id(vehicle_id):  # ID focused fetching
    conn = get_db_connection()  # Acquire DB connection 
    row = conn.execute("SELECT * FROM Vehicle WHERE VehicleID = ?", (vehicle_id,)).fetchone()  # Filtering mechanism
    conn.close()  # Free object pool 
    return row_to_dict(row)  # Serialized view


def update_vehicle(vehicle_id, license_plate=None, model=None):
    fields = []
    params = []

    if license_plate is not None:
        fields.append("LicensePlate = ?")
        params.append(license_plate)
    if model is not None:
        fields.append("Model = ?")
        params.append(model)

    if not fields:
        return get_vehicle_by_id(vehicle_id)

    params.append(vehicle_id)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"UPDATE Vehicle SET {', '.join(fields)} WHERE VehicleID = ?", params)
    conn.commit()
    row = cur.execute("SELECT * FROM Vehicle WHERE VehicleID = ?", (vehicle_id,)).fetchone()
    conn.close()
    return row_to_dict(row)


def delete_vehicle(vehicle_id):  # Targeted object removal
    conn = get_db_connection()  # Prep DB environment
    cur = conn.cursor()  # Action module 
    cur.execute("DELETE FROM Vehicle WHERE VehicleID = ?", (vehicle_id,))  # Remove exact element 
    conn.commit()  # Fire modifications to storage
    return cur.rowcount > 0  # Did action happen?

#--Route Crud--

def create_route(date, service_zone):  # Handles Route configurations
    conn = get_db_connection()  # Connection startup
    cur = conn.cursor()  # Load cursor operation
    cur.execute("INSERT INTO DeliveryRoute (Date, ServiceZone) VALUES (?, ?)", (date, service_zone))  # Load object
    conn.commit()  # Push row 
    rid = cur.lastrowid  # Generated identifier 
    row = cur.execute("SELECT * FROM DeliveryRoute WHERE RouteID = ?", (rid,)).fetchone()  # Confirm 
    conn.close()  # Clear environment 
    return row_to_dict(row)  # Return data 


def get_all_routes():  # Unpack existing delivery configurations 
    conn = get_db_connection()  # Standard DB instance
    rows = conn.execute("SELECT * FROM DeliveryRoute").fetchall()  # Gather arrays 
    conn.close()  # Terminate DB block
    return [row_to_dict(r) for r in rows]  # Convert structure 

#--Package Crud--

def create_package(description, weight, route_id=None):  # Appends a package target
    conn = get_db_connection()  # Instantiate bridge 
    cur = conn.cursor()  # Ready session 
    cur.execute(  # Fire execution
        "INSERT INTO Package (Description, Weight, RouteID) VALUES (?, ?, ?)",  # Statement args defined
        (description, weight, route_id),  # Execution list target variables 
    )
    conn.commit()  # Lock change 
    pid = cur.lastrowid  # Retrieve memory ID
    row = cur.execute("SELECT * FROM Package WHERE PackageID = ?", (pid,)).fetchone()  # Fetch latest state
    conn.close()  # Terminate bridge instance
    return row_to_dict(row)  # Formatting element list 

def get_all_packages():  # Get all packages
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM Package").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

#--DriverRoute Crud--

def create_driver_route(driver_id, route_id, date):  # Mapping function between driver & Route schedule 
    conn = get_db_connection()  # Call handler 
    cur = conn.cursor()  # Assign object context wrapper
    cur.execute(  # Set payload string mechanism
        "INSERT INTO DriverRoute (DriverID, RouteID, Date) VALUES (?, ?, ?)",  # Bind values template 
        (driver_id, route_id, date),  # Payload properties attached 
    )
    conn.commit()  # Finalize operation cycle 
    drid = cur.lastrowid  # Identifier fetch
    row = cur.execute("SELECT * FROM DriverRoute WHERE DriverRouteID = ?", (drid,)).fetchone()  # Review creation 
    conn.close()  # Quit process stream
    return row_to_dict(row)  # JSON-compatible mapping return