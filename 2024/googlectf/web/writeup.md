## sappy

I am a beginner programmer and I share what I learnt about JavaScript with the world!

Note: Flag is in the cookie

Basically this a javascript challenge where it has functionality to share javascript.
Once you enter a URL it will use a bot that has the flag in its cookie to browse to that URL.

It uses the net module to make a client and browse to the URL:

```js
const net = require('net');
const XSSBOT_PORT = process.env.XSSBOT_PORT;
const XSSBOT_HOST = process.env.XSSBOT_HOST;
function visit(url) {
  console.log(url);
  const client = net.Socket();
  client.connect(XSSBOT_PORT, XSSBOT_HOST);
  client.on('data', data => {
    let msg = data.toString().trim();
    if (msg == "Please send me a URL to open.") {
      client.write(url+'\n');
      client.destroy();
    }
    console.log(msg);
  });
}
module.exports = {visit}
```

There are five endpoints:
- `/` shows the main page
- `/sap.html` use to be loaded with iframe in the main page
- `/sap/:p` receives a parameter which compares with a list of json objects, they are loaded to sap.html which are loaded to the main page
- `/pages.json` shows the pages.json file
- `/share` receives an url and uses the bot to browse to that url

## Grand Prix Heaven

I LOVE F1 ♡ DO YOU LOVE RACING TOO?

Seems like a race conditions challenge...

## Postviewer v3

New year new postviewer.

