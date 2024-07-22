import os
import requests
import json
import hashlib


session = requests.Session()

register_url = 'http://casino.web.jctf.pro/register'
login_url = 'http://casino.web.jctf.pro/login'
info_url = "http://casino.web.jctf.pro/info"
new_server_seed_url = "http://casino.web.jctf.pro/revealServerSeed"


payload = {
    'username': 'testworthuser7',
    'password': 'your_password'
}

session.post(register_url, data=payload).text

session.post(login_url, data=payload).text

user_info = json.loads(session.get(info_url).text)

# with open("serverSeedsours.txt", "w+") as file:
#     for i in range(10000000):
#         # Generate 32 random bytes
#         random_bytes = os.urandom(32)

#         # Convert the bytes to a hexadecimal string
#         hex_string = random_bytes.hex()

#         sha256_hash = hashlib.sha256()

#         # Update the hash object with the server seed
#         sha256_hash.update(hex_string.encode('utf-8'))

#         # Get the hexadecimal digest of the hash
#         hex_digest = sha256_hash.hexdigest()

#         file.write(f"{hex_digest} - {hex_string}\n")

found = False
with open("serverSeedsours.txt", "r+") as file:    
    while True:
        serverseeds = json.loads(session.get(new_server_seed_url).text)
        newhash = serverseeds["newServerSeedHash"]
        for line in file:
            if newhash in line:
                found = True

        if found:
            print(f"Found it!: {newhash}")
            break