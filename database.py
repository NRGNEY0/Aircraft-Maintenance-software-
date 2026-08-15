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

conn.execute(""" 
CREATE TABLE IF NOT EXISTS InspectionSchedule ( 
ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
Registration TEXT,
InspectionType TEXT,
IntervalHours REAL,
IntervalDays INTEGER,
FOREIGN KEY (Registration) REFERENCES Aircraft(Registration)

)





""")

conn.execute("""
      UPDATE InspectionSchedule 
      SET InspectionType = 'Horizontal Stabiliser Jackscrew Assembly Inspection'
      WHERE Registration = 'G-NEYO'

 """)

conn.commit()

conn.close()









