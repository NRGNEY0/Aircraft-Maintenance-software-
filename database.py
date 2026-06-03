import sqlite3


def init_db():
    conn = sqlite3.connect("aircrafts.db")

    cursor = conn.cursor()
    cursor.executemany("""
    INSERT OR IGNORE INTO Aircraft
    VALUES(?,?,?,?,?)""",[
    ('G-RYAN', 'Airbus', 'A320-200', 'CFM56-5A', 'Active'),
    ('G-TADZ', 'Airbus', 'A330-300', 'Rolls-Royce Trent 700', 'Active'),
    ('G-DAMZ', 'Boeing', 'B737-800', 'CFM56-7B', 'Active'),
    ('G-BOAT', 'Airbus', 'A380-800', 'Rolls-Royce Trent 900', 'Active'),]
    
    )



    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()




