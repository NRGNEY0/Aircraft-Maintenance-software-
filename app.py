import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

print("Flask works")
def generateTaskID(): #Function that generates task id for the maintenance database
  with sqlite3.connect("aircrafts.db") as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT MaintenanceID FROM Maintenance ORDER BY rowid DESC LIMIT 1")
    last= cursor.fetchone()

    if last is None:
      return "MX-0001"
    
    last_num = int(last[0].split("-")[1])
    new_num = last_num + 1
    return f"MX-{new_num:04d}"

def generateFlightID():
  with sqlite3.connect("aircrafts.db") as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT FlightID FROM Flight_log ORDER BY rowid DESC LIMIT 1")
    last = cursor.fetchone()

    if last is None:
      return "FL-0001"
    
    else:
      last_num = int(last[0].split("-")[1]) 
      new_num = last_num + 1 
      return f"FL-{new_num:04d}"


def getInspectionStatus(registration, totalHours, hoursSinceLastMaintenance):
  with sqlite3.connect("aircrafts.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    result = []
    today = datetime.today()

    cursor.execute("SELECT * FROM InspectionSchedule WHERE Registration = ?",(registration,))
    inspections = cursor.fetchall()

    for inspection in inspections:
      InspectionType=inspection['InspectionType']
      dayinterval=inspection['IntervalDays']
      hourinterval=inspection['IntervalHours']



    cursor.execute("SELECT * FROM Maintenance WHERE Registration = ?",(registration,))
    tasks = cursor.fetchall()

    for task in tasks:
      tasktype = task['Task']

    cursor.execute("SELECT DatePerformed FROM Maintenance WHERE Registration = ? AND Task = ? ORDER BY DatePerformed",(registration, InspectionType,))
    lastDone = cursor.fetchone() or None

    datedone = lastDone['DatePerformed']

   
    if lastDone is None:
      result.append({
        "InspectionType": inspection['InspectionType'],
        "lastDone": "Never done",
        "DateDue": "N/A",
        "DaysRemaining": "N/A",
        "HoursRemaining": "N/A",
        "Status": "OverDue"
      })
      
      
    
    dateDue = datetime.strptime(lastDone['DatePerformed'], "%Y-%m-%d") + timedelta(days=dayinterval)
    daysremaining = (dateDue - today).days 

    HoursRemaining = (hourinterval + hoursSinceLastMaintenance) - totalHours

    if daysremaining <= 0 or HoursRemaining <= 0:
      status = "Overdue"
    elif daysremaining <= 14 or HoursRemaining <= 20:
      status = "Due Soon"
    else:
      status = "OK"
    
    results.append({
      "InspectionType": InspectionType,
      "lastDone": lastDone,
      "DateDue": dateDue.strftime("%Y-%m-%d"),
      "DaysRemaining": daysremaining,
      "HoursRemaining": HoursRemaining,
      "Status": status
    })

    return results

@app.route("/") #This route is for the home page 
def home():

  with sqlite3.connect("aircrafts.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Aircraft")
    total_aircraft = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Aircraft WHERE Status ='Grounded'")
    grounded_Aircraft = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM Maintenance DESC LIMIT 10")
    recentTasks = cursor.fetchall()
    
    return render_template(
      "home.htm",
      total_aircraft=total_aircraft,
      grounded_Aircraft=grounded_Aircraft,
      recentTasks=recentTasks
      
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




@app.route("/add_task", methods=['GET', 'POST'])
def add_task():
  if request.method == "POST":
    maintenanceID = generateTaskID()
    registration = request.form['Registration']
    task = request.form['Task']
    status = request.form['Status']
    date = request.form['Date']
    technician = request.form['Technician']
    note = request.form['Notes']

    with sqlite3.connect("aircrafts.db") as conn:
      cursor = conn.cursor()
      cursor.execute("INSERT INTO Maintenance VALUES(?,?,?,?,?,?,?)",(maintenanceID, registration, task, status, date, technician, note))
      conn.commit()

      return redirect(url_for("maintenance"))
  return render_template("add_task.htm")


@app.route("/aircraft/<registration>")
def aircraft_detail(registration):
  with sqlite3.connect("aircrafts.db") as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Aircraft WHERE Registration = ?",(registration,))
    aircraft = cursor.fetchone()

    cursor.execute("SELECT * FROM Flight_Log WHERE Registration = ?", (registration,))
    flights = cursor.fetchall()

    cursor.execute("SELECT * FROM Maintenance WHERE Registration = ?",(registration,))
    m_records = cursor.fetchall()

    cursor.execute("SELECT SUM(HoursFlown) FROM Flight_log WHERE Registration = ?",(registration,))
    totalHours = cursor.fetchone()[0]

    cursor.execute("SELECT DatePerformed FROM Maintenance WHERE Registration = ? ORDER BY DatePerformed DESC LIMIT 1",(registration,))
    last_maintenance = cursor.fetchone()

    cursor.execute("SELECT SUM(HoursFlown) FROM Flight_Log WHERE Registration = ? AND FlightDate >= ?",(registration, last_maintenance[0] if last_maintenance else None)) #Gets the hours flown since last maintenance 
    hours_since_last_maintenance = cursor.fetchone()[0]

    inspection_status = getInspectionStatus(registration, totalHours, hours_since_last_maintenance)

    return render_template("aircraft_detail.htm", aircraft=aircraft, m_records=m_records, flights=flights, totalHours=totalHours, hours_since_last_maintenance=hours_since_last_maintenance, inspection_status=inspection_status) 

@app.route("/flight_log/<registration>")
def flight_log(registration):
  with sqlite3.connect('aircrafts.db') as conn:
    conn.row_factory= sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Aircraft WHERE Registration = ?",(registration,))
    aircraft=cursor.fetchone()
  return render_template("flight_log.htm", aircraft=aircraft)


@app.route("/log_flight/<registration>", methods=["GET", "POST"])
def log_flight(registration):
  if request.method== "POST":
    flightID = generateFlightID()
    Date = request.form['Date']
    HoursFlown = request.form['HoursFlown']
    Notes = request.form['Notes']

    with sqlite3.connect("aircrafts.db") as conn:
      cursor = conn.cursor()

      cursor.execute("INSERT INTO Flight_Log VALUES (?,?,?,?,?)", (flightID, registration, Date, HoursFlown, Notes))

      return redirect(url_for('aircraft_detail', registration=registration))
    return render_template('flight_log.htm')



if __name__ == "__main__":
    app.run(debug=True, port=5001)