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

"""def clear_table():
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

clear_table()"""

import requests
import sqlite3

local_database = sqlite3.connect('employee.db')

def sync_data():
    # Retrieve local changes
    cursor = local_database.cursor()
    cursor.execute('SELECT * FROM employee WHERE synced = 0')
    local_changes = cursor.fetchall()

    # Synchronize with the central database
    try:
        response = requests.post('http://your-api-endpoint/sync', json=local_changes)
        if response.json()['status'] == 'success':
            # Update local changes as synced
            cursor.execute('UPDATE employee SET synced = 1 WHERE synced = 0')
            local_database.commit()
    except Exception as e:
        print(f'Synchronization error: {e}')

sync_data()
