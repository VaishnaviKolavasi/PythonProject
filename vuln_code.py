# VULN 1: Hardcoded Credentials
db_username = "admin"
db_password = "SuperSecret123"  # hardcoded, bad practice

# VULN 2: SQL Injection (simulated)
import sqlite3

def login(user_input):
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute("CREATE TABLE users (username TEXT, password TEXT)")
    c.execute("INSERT INTO users VALUES ('admin', 'SuperSecret123')")

    # Vulnerable query - directly using input
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    print("[SQL Injection] Executing:", query)
    c.execute(query)
    result = c.fetchall()
    print("[SQL Injection] Result:", result)

# VULN 3: Reflected XSS (simulated via terminal)
def echo_user_input():
    user_input = input("Enter your name: ")
    print(f"<h1>Hello {user_input}</h1>")  # Would be vulnerable in web output

# VULN 4: Insecure Deserialization
import pickle

def unsafe_deserialize(data):
    # NEVER do this in real code
    obj = pickle.loads(data)
    print("[Deserialization] Loaded object:", obj)

# VULN 5: Missing HttpOnly/Secure flags on cookies (simulated)
class FakeResponse:
    def set_cookie(self, name, value):
        # Missing secure and httponly flags
        print(f"[Cookie] Set-Cookie: {name}={value}; Path=/")

# VULN 6: Path Traversal
def read_file(filename):
    # User can pass ../../../etc/passwd to read system files
    with open("files/" + filename, "r") as f:
        print(f.read())


# ---- Simulated Test Calls ----
login("admin' OR '1'='1")  # SQL Injection
echo_user_input()          # XSS
unsafe_deserialize(pickle.dumps({'user': 'admin'}))  # Not malicious but unsafe
resp = FakeResponse()
resp.set_cookie("sessionid", "abc123")  # Missing secure flags
read_file("../../../../etc/passwd")     # Path traversal
