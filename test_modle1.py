import requests
import sqlite3
import os

# connect
def authenticate(username, email, password, full_name):
    url = 'ServersIP'  # Replace with your server's IP address or domain

    data = {
        'username': username,
        'email': email,
        'password': password,
        'full_name': full_name
    }

    response = requests.post(url, json=data)

    if response.status_code == Code:
        result = response.json()
        print(result['message'])
    else:
        print("Error:", response.text)
# Example usage
username_input = input("Enter username: ")
email_input = input("Enter email: ")
password_input = input("Enter password: ")
fullName_input = input("Enter full name: ")

conn = sqlite3.connect('local_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS local_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        full_name TEXT
    )
''')

try:
    cursor.execute("INSERT INTO local_users (username, email, password, full_name) VALUES (?, ?, ?, ?)",(username_input, email_input, password_input, fullName_input))
    conn.commit()
    print("Registration saved locally.")
except sqlite3.IntegrityError:
    print("Username or email already exists locally.")
conn.close()
authenticate(username_input, email_input, password_input, fullName_input)
