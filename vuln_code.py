# app.py
from flask import Flask, request, make_response, render_template_string
import os
import sqlite3
import subprocess
import pickle

app = Flask(__name__)

# VULN 1: Hardcoded credentials
aws_secret_key = "AKIAIOSFODNN7EXAMPLE"
db_password = "P@ssw0rd123!"


@app.route('/rce')
def rce():
    # VULN 2: Remote Code Execution via unsanitized input to subprocess
    cmd = request.args.get('cmd')
    return subprocess.getoutput(cmd)

@app.route('/xss')
def xss():
    # VULN 3: Reflected XSS
    name = request.args.get('name')
    return render_template_string("<h1>Hello " + name + "</h1>")

@app.route('/ssrf')
def ssrf():
    # VULN 4: SSRF - User controls the URL being fetched by the server
    import requests
    url = request.args.get('url')  # e.g., ?url=http://localhost:5000/admin
    r = requests.get(url)
    return r.text

@app.route('/file_read')
def file_read():
    # VULN 5: Directory traversal
    filename = request.args.get('file')
    with open("files/" + filename, 'r') as f:
        return f.read()

@app.route('/cookie')
def cookie():
    # VULN 6: Missing HttpOnly flag
    resp = make_response("Setting insecure cookie")
    resp.set_cookie("session", "abc123")  # No HttpOnly, No Secure
    return resp

@app.route('/deserialize')
def deserialize():
    # VULN 7: Insecure deserialization
    data = request.args.get('data')
    obj = pickle.loads(bytes(data, 'utf-8'))
    return str(obj)

@app.route('/sql')
def sql_injection():
    # VULN 8: SQL Injection
    name = request.args.get('name')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{name}'"
    c.execute(query)
    return str(c.fetchall())

@app.route('/debug')
def debug():
    # VULN 9: Debug mode exposed
    return app.run(debug=True)

@app.route('/eval')
def eval_vuln():
    # VULN 10: Arbitrary code execution via eval
    code = request.args.get('code')
    return str(eval(code))
