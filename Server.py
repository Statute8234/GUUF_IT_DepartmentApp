from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)
conn = sqlite3.connect('employee.db')
cursorDB = conn.cursor()
def createDB():
    try:
        cursorDB.execute('''CREATE TABLE IF NOT EXISTS employee (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        email TEXT,
                        password TEXT,
                        full_name TEXT
                    )''')
    except:
        pass
createDB()

# Add a sample user
cursorDB.execute("INSERT OR IGNORE INTO employee (username, email, password, full_name) VALUES (?, ?, ?, ?)", ('admin', 'admin_email@gmail.com', 'password123', 'admin admin'))
# Commit changes and close connection
conn.commit()
conn.close()

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    
    if username and password:
        # Login authentication
        cursor.execute("SELECT * FROM employee WHERE username=? AND password=?", (username, password))
    elif username and email:
        # Forgot password authentication
        cursor.execute("SELECT * FROM employee WHERE username=? AND email=?", (username, email))
    elif full_name and email:
        # Sign up authentication
        cursor.execute("SELECT * FROM employee WHERE full_name=? AND email=?", (full_name, email))
    else:
        conn.close()
        return jsonify({"status": "error", "message": "Invalid request. Missing credentials."})
    
    user_data = cursor.fetchone()
    if user_data:
        response = {"status": "success", "message": "Authentication successful!"}
    else:
        response = {"status": "error", "message": "Authentication failed. Incorrect credentials."}

    conn.close()
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
