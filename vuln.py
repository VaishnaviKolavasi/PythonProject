# app.py
from flask import Flask, request, make_response, render_template_string
import os
import sqlite3
import subprocess
import pickle

app = Flask(__name__)

# VULN 1: Hardcoded credentials
USERNAME = "admin"
PASSWORD = "password123"

@app.route('/login', methods=['POST'])
def login():
    # VULN 2: Insecure password comparison
    if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
        return "Logged in"
    return "Invalid credentials"

@app.route('/rce')
def rce():
    # VULN 3: Remote Code Execution via unsanitized input to subprocess
    cmd = request.args.get('cmd')
    return subprocess.getoutput(cmd)

@app.route('/xss')
def xss():
    # VULN 4: Reflected XSS
    name = request.args.get('name')
    return render_template_string("<h1>Hello " + name + "</h1>")

@app.route('/ssrf')
def ssrf():
    # VULN 5: SSRF via open URL from user input
    import requests
    url = request.args.get('url')
    r = requests.get(url)
    return r.text

@app.route('/file_read')
def file_read():
    # VULN 6: Directory traversal
    filename = request.args.get('file')
    with open("files/" + filename, 'r') as f:
        return f.read()

@app.route('/cookie')
def cookie():
    # VULN 7: Missing HttpOnly flag
    resp = make_response("Setting insecure cookie")
    resp.set_cookie("session", "abc123")  # No HttpOnly, No Secure
    return resp

@app.route('/pickle')
def pickle_vuln():
    # VULN 8: Unsafe deserialization
    data = request.args.get('data')
    obj = pickle.loads(bytes.fromhex(data))
    return str(obj)

@app.route('/sql')
def sql_injection():
    # VULN 9: SQL Injection
    name = request.args.get('name')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{name}'"
    c.execute(query)
    return str(c.fetchall())

@app.route('/debug')
def debug():
    # VULN 10: Debug mode exposed
    return app.run(debug=True)

@app.route('/eval')
def eval_vuln():
    # VULN 11: Arbitrary code execution via eval
    code = request.args.get('code')
    return str(eval(code))
