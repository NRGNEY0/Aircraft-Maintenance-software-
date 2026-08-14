import sqlite3


conn = sqlite3.connect("aircrafts.db")

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Flight_Log (
FlightID  PRIMARY KEY,
Registration TEXT,
FlightDate TEXT,
HoursFlown REAL,
DepartureAirport TEXT,
ArrivalAirport TEXT,
Notes TEXT,
FOREIGN KEY (Registration) REFERENCES Aircraft(Registration) )""")

cursor.executemany("""INSERT INTO Inspections
 VALUES ()  """)
conn.commit()

cursor.execute("DROP * FROM Flight_log  WHERE FlightID = FL-0002")
conn.close()









