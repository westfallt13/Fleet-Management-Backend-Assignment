import sqlite3  # Import Python's built-in SQLite3 module for database operations

DB_PATH = "logistics.db"  # Define a constant string representing the path to the local SQLite database file

# Database connection and initialization
def get_db_connection():  # Define a helper function to create and return a configured database connection 
    conn = sqlite3.connect(DB_PATH)  # Establish a connection to the SQLite database file
    conn.row_factory = sqlite3.Row  # Configure the connection to return rows as dictionaries instead of plain tuples
    conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key constraints enforcement in SQLite
    return conn  # Return the configured connection object for executing queries

# Database initialization
def init_db():  # Define the function responsible for setting up the initial database schema
    conn = get_db_connection()  # Acquire a new database connection
    cur = conn.cursor()  # Create a cursor object from the connection to execute SQL statements

# Create tables if they don't exist
    cur.execute(""" 
    CREATE TABLE IF NOT EXISTS Vehicle (  -- Execute a SQL command to create the Vehicle table if it does not already exist
        VehicleID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Define VehicleID as an auto-incrementing integer primary key
        LicensePlate TEXT NOT NULL UNIQUE,  -- Define LicensePlate as a required text field that must be globally unique
        Model TEXT NOT NULL  -- Define Model as a required text field
    );
    """)
# Create tables if they don't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Driver (  -- Execute a SQL command to create the Driver table if it does not already exist
        DriverID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Define DriverID as an auto-incrementing integer primary key
        Name TEXT NOT NULL,  -- Define Name as a required text field
        LicenseType TEXT NOT NULL,  -- Define LicenseType as a required text field
        VehicleID INTEGER UNIQUE,  -- Define VehicleID as an integer field that must be unique (1-to-1 relationship with Vehicle)
        FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID) ON DELETE SET NULL  -- Create a foreign key linking to Vehicle ID; set to null if Vehicle is deleted
    );
    """)
# Create tables if they don't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS DeliveryRoute (  -- Execute a SQL command to create the DeliveryRoute table if it does not already exist
        RouteID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Define RouteID as an auto-incrementing integer primary key
        Date TEXT NOT NULL,  -- Define Date as a required text field (usually stored as ISO 8601 string in SQLite)
        ServiceZone TEXT NOT NULL  -- Define ServiceZone as a required text field representing the geographical area
    );
    """)
# Create tables if they don't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Package (  -- Execute a SQL command to create the Package table if it does not already exist
        PackageID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Define PackageID as an auto-incrementing integer primary key
        Description TEXT,  -- Define Description as an optional text field describing the package contents
        Weight REAL,  -- Define Weight as a floating point number field representing package weight
        RouteID INTEGER,  -- Define RouteID as an integer field linking to DeliveryRoute
        FOREIGN KEY (RouteID) REFERENCES DeliveryRoute(RouteID) ON DELETE SET NULL  -- Set the RouteID to NULL if the associated route is deleted
    );
    """)
# Create tables if they don't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS DriverRoute (  -- Execute a SQL command to create the junction table linking Drivers and Routes
        DriverRouteID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Define DriverRouteID as an auto-incrementing primary key
        DriverID INTEGER NOT NULL,  -- Define DriverID as a required reference to the Driver
        RouteID INTEGER NOT NULL,  -- Define RouteID as a required reference to the DeliveryRoute
        Date TEXT NOT NULL,  -- Define Date as a required text field for when the specific driver performs the route
        FOREIGN KEY (DriverID) REFERENCES Driver(DriverID) ON DELETE CASCADE,  -- Automatically delete this mapping if the corresponding Driver is deleted
        FOREIGN KEY (RouteID) REFERENCES DeliveryRoute(RouteID) ON DELETE CASCADE,  -- Automatically delete this mapping if the corresponding DeliveryRoute is deleted
        UNIQUE (DriverID, RouteID, Date)  -- Ensure that a specific driver cannot be assigned to the same route more than once on the same date
    );
    """)

    conn.commit()  # Save (commit) all the table creation changes to the database
    conn.close()  # Close the connection and free up database resources
