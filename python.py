import sqlite3
from flask import Flask

app = Flask(__name__)

print("Flask works")

conn = sqlite3.connect("aircrafts.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Aircraft (
  Registration TEXT PRIMARY KEY,

  Manufacturer TEXT,

  Model TEXT,

  Engine_Type TEXT,

  Status TEXT)
""")



cursor.execute("""
 INSERT INTO Aircraft
 VALUES( "G-NEYO", "Boeing", "B787-9","Rolls-Royce Trent 1000", "Grounded")

""")


conn.commit()
conn.close()