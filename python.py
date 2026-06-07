import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

print("Flask works")

@app.route("/") #This route is for the home page 
def home():

  conn = sqlite3.connect("aircrafts.db")

  cursor = conn.cursor()

  cursor.execute("SELECT COUNT(*) FROM Aircraft")
  total_aircraft = cursor.fetchone()[0]

  cursor.execute("SELECT COUNT(*) FROM Aircraft WHERE Status ='Grounded'")
  grounded_Aircraft = cursor.fetchone()[0]


  
  
  conn.close()
  return render_template(
    "home.htm",
    total_aircraft=total_aircraft,
    grounded_Aircraft=grounded_Aircraft
  )


@app.route("/aircraft")
def aircraft():

  conn = sqlite3.connect("aircrafts.db")
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM Aircraft")
  Aircrafts = cursor.fetchall()
  

  conn.close()


  return render_template("aircraft.htm", Aircrafts=Aircrafts)


@app.route("/maintenance")
def maintenance():
  return render_template("maintenance.htm")


@app.route("/add aircraft")
def add_aircraft():
  return render_template("add aircraft.htm")



if __name__ == "__main__":
    app.run(debug=True, port=5001)