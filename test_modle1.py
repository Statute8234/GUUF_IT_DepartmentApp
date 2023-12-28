"""import sqlite3

conn = sqlite3.connect('employee.db')
cursorDB = conn.cursor()
def create():
    cursorDB.execute('''CREATE TABLE employee  (
                        username text,
                        email text,
                        password text,
                        full name text
                    )''')
create()
cursorDB.execute("INSERT INTO employee VALUES ('admin', 'admin_email@gmail.com', 'admin', 'admin admin')")
cursorDB.execute("SELECT * FROM employee WHERE username='admin'")
print(cursorDB.fetchall())
conn.commit()
conn.close()"""

import sqlite3

def clear_table():
    conn = sqlite3.connect('employee.db')  # Replace 'your_database.db' with the actual name of your SQLite database
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM employee")  # Replace 'your_table_name' with the actual name of your table
        conn.commit()
        print("All records cleared successfully.")
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        conn.close()

clear_table()
