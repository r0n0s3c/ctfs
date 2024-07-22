# Intro

Picking a starter is hard, I hope you can do it.

Flag format: PCTF{}

Author: @angr404

# Challenge

Once we open the website we get the iconic pokemon moment where we choose the first pokemon we want.
We have three pokemons and once we click on one, it will go to a page where it shows their stats.
To access for example squirtle page the following request is made:

```
GET /squirtle HTTP/1.1
Host: chal.pctf.competitivecyber.club:5555
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://chal.pctf.competitivecyber.club:5555/
DNT: 1
Connection: close
Cookie: Flag 5/5=e4a541}; PHPSESSID=f456a81b6c2e4dbaa51e2998a3032bb8
Upgrade-Insecure-Requests: 1

```

The headers of the page have an hint: `Server: Werkzeug/2.3.7 Python/3.11.5`
It seems like a python application. When request for a different pokemon that is not one of the three: GET /hello HTTP/1.1.
We get: `"hello" isn't a starter Pokémon.`. This may be a SSTI. Lets try a few a payloads. Once we try: `{{7*7}}` we get 49 as a response.
This means that it may have a template injection. Using: `{{self.__init__.__globals__}}` we get all the built in classes and know for sure that is jinja2.
