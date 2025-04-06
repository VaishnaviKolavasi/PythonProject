from flask import Flask, request, send_file
import os
import sqlite3

app = Flask(__name__)

# --- Setup (for SQL Injection demo) ---
DATABASE = 'users.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'secret')")
    conn.commit()
    conn.close()

# --- Vulnerable route: Directory Traversal ---
@app.route('/download')
def download():
    filename = request.args.get('file')  # e.g., ../../etc/passwd
    return send_file(os.path.join('files', filename))

# --- Vulnerable route: Command Injection ---
@app.route('/ping')
def ping():
    host = request.args.get('host')  # e.g., 127.0.0.1; ls
    return os.popen(f"ping -c 1 {host}").read()

# --- Vulnerable route: SQL Injection ---
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = c.execute(query).fetchone()
    conn.close()
    if result:
        return "Logged in!"
    else:
        return "Invalid credentials."

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
