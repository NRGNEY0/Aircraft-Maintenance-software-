import sqlite3


def init_db():
    conn = sqlite3.connect("aircrafts.db")

    cursor = conn.cursor()

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS Maintenance(
        MaintenanceID TEXT PRIMARY KEY,
        Registration TEXT,
        Task TEXT,
        Status TEXT,
        DatePerformed TEXT,
        Technician TEXT,
        Notes TEXT,
        FOREIGN KEY (Registration) REFERENCES Aircraft(Registration))
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Inspections(
    InspectionID TEXT PRIMARK KEY,
    Registration TEXT,
    InspectionTYPE TEXT,
    DueDate TEXT,
    Last_Completed TEXT,
    Status TEXT,
    FOREIGN KEY (Registration) REFERENCES Aircraft(Registration))
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Parts(
    PartID TEXT PRIMARY KEY,
    PartName TEXT,
    PartNumber INTEGER,
    Quantity INTEGER,
    Condition TEXT,
    CompatableAircraft TEXT,
    FOREIGN KEY (CompatableAircraft) REFERENCES Aircraft(Registration))
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()




