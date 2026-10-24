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

conn.executemany("""
      INSERT INTO InspectionSchedule (Registration, InspectionType, IntervalHours, IntervalDays) VALUES (?, ?, ?, ?)
 """,
 [

 ("G-RYAN", "100 Hour Inspection", 100, 0),
 ("G-RYAN", "Brake Inspection", 300, 0),
 ("G-RYAN", "Lubrication Inspection", 250, 0),
 ("G-RYAN", "Engine oil Inspection", 250, 0)
 
 ],)

conn.commit()

conn.close()









