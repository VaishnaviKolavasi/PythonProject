from flask import Flask, request, make_response, render_template_string
import os
import sqlite3
import subprocess
import pickle
import requests

app = Flask(__name__)

# VULN 1: Hardcoded credentials like secret keys and passwords
aws_secret_key = "AKIAIOSFODNN720178KEYSECRET"
db_password = "P@ssw0rd123!"


@app.route('/rce')
def rce():
    # VULN 2: Remote Code Execution via unsanitized input to subprocess can let the user run any command on the server like ls sensitive files
    cmd = request.args.get('cmd')
    return subprocess.getoutput(cmd)

@app.route('/xss')
def xss():
    # VULN 3: Reflected XSS can lead to unsantized malicious js being rendered in the HTTP response.
    name = request.args.get('name')
    return render_template_string("<h1>Hello " + name + "</h1>")

@app.route('/ssrf')
def ssrf():
    # VULN 4: SSRF - User controls the URL being fetched by the server. For eg: services that can be internal can be fetched using the local host url
    url = request.args.get('url')  # e.g., ?url=http://localhost:5000/admin
    r = requests.get(url)
    return r.text

@app.route('/file_read')
def file_read():
    # VULN 5: Directory traversal vuln that can make the user to access files outside of their authorised scope using ../ string
    filename = request.args.get('file')
    with open("files/" + filename, 'r') as f:
        return f.read()

@app.route('/cookie')
def cookie():
    # VULN 6: Missing HttpOnly flag enables a cookie to be sent over HTTP or included in JS
    resp = make_response("Setting insecure cookie")
    resp.set_cookie("session", "abc123")  # No HttpOnly, No Secure
    return resp

@app.route('/deserialize')
def deserialize():
    # VULN 7: Insecure deserialization allows the user input to be converted into objects without validation
    data = request.args.get('data')
    obj = pickle.loads(bytes(data, 'utf-8'))
    return str(obj)

@app.route('/sql')
def sql_injection():
    # VULN 8: SQL Injection can result in retrieval of sensitive data and manipulation of database and its schema
    name = request.args.get('name')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{name}'"
    c.execute(query)
    return str(c.fetchall())

@app.route('/debug')
def debug():
    # VULN 9: Debug mode provides the user a full interactve shell. This is useful while code development but not in production.
    return app.run(debug=True)

@app.route('/eval')
def eval_vuln():
    # VULN 10: Any malicious script passed through eval is executed. As eval takes a string and executes it as code.
    code = request.args.get('code')
    return str(eval(code))
