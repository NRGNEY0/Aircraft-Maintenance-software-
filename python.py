import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

print("Flask works")

@app.route("/")
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

if __name__ == "__main__":
    app.run(debug=True, port=5001)