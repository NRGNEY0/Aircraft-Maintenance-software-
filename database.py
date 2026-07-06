import sqlite3


conn = sqlite3.connect("aircrafts.db")

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Flight_LogS (
FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
Registration TEXT,
FlightDate TEXT,
HoursFlown REAL,
Notes TEXT,
FOREIGN KEY (Registration) REFERENCES Aircraft(Registration) )""")

conn.commit()
conn.close()








