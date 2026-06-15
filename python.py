import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

print("Flask works")
def generateTaskID(): #Function that generates task id
  with sqlite3.connect("aircrafts.db") as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT MaintenanceID FROM Maintenance ORDER BY rowid DESC LIMIT 1")
    last= cursor.fetchone()

    if last is None:
      return "MX-0001"
    
    last_num = int(last[0].split("-")[1])
    new_num = last_num + 1
    return f"MX-{new_num:04d}"


@app.route("/") #This route is for the home page 
def home():

  with sqlite3.connect("aircrafts.db") as conn:

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Aircraft")
    total_aircraft = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Aircraft WHERE Status ='Grounded'")
    grounded_Aircraft = cursor.fetchone()[0]


    
    
    
    return render_template(
      "home.htm",
      total_aircraft=total_aircraft,
      grounded_Aircraft=grounded_Aircraft
    )


@app.route("/aircraft")
def aircraft():

  with sqlite3.connect("aircrafts.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Aircraft")
    Aircrafts = cursor.fetchall()
    

    


    return render_template("aircraft.htm", Aircrafts=Aircrafts)


@app.route("/maintenance")
def maintenance():
  with sqlite3.connect("aircrafts.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Maintenance")
    Tasks = cursor.fetchall()


    return render_template("maintenance.htm", Tasks=Tasks)


  


@app.route("/add_aircraft", methods=["GET", "POST"])
def add_aircraft():
  if request.method == "POST":
    registration = request.form["Registration"]
    manufacturer = request.form['Manufacturer']
    model = request.form['Model']
    engine = request.form['Engine']
    status = request.form['Status']

    with sqlite3.connect("aircrafts.db") as conn:
      cursor = conn.cursor()
      cursor.execute("INSERT INTO Aircraft VALUES(?, ?, ?, ?, ?)",
      (registration, manufacturer, model, engine, status))
      conn.commit()
      

      return redirect(url_for("aircraft"))

  return render_template("add_aircraft.htm")

@app.route("/add_task" methods=['GET', 'POST'])
def add_task





if __name__ == "__main__":
    app.run(debug=True, port=5000)