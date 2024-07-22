## title

Percetron

## Description

Your faction's mission is to infiltrate and breach the heavily fortified servers of KORP's web application, known as "Percetron." This application stores sensitive information, including IP addresses and digital certificates, crucial for the city's infrastructure.

## Solution

Info:
- Neo4j version 5.13.0, bolt://127.0.0.1:7687
- curl version 7.70.0
- alpinelinux version v3.9
- mongodb, mongodb://127.0.0.1:27017/percetron
- environment variables file in .env
- flag at /flag.txt
- web app on port 1337
- haproxy config block endpoint: `http-request deny if { path -i -m beg /healthcheck-dev }`
- web app is made in nodejs, bellow are the packages:

```json
{
  "name": "web_percetron",
  "version": "5.4.0",
  "description": "",
  "main": "index.js",
  "dependencies": {
    "@faker-js/faker": "^8.3.1",
    "@steezcram/sevenzip": "^1.1.6",
    "axios": "^1.6.2",
    "bcryptjs": "^2.4.3",
    "dotenv": "^16.3.1",
    "express": "^4.18.2",
    "express-session": "^1.17.3",
    "mongoose": "^8.0.3",
    "neo4j-driver": "^5.14.0",
    "node-forge": "^1.3.1",
    "pug": "^3.0.2"
  },
  "scripts": {
    "start": "node ."
  },
  "keywords": [],
  "author": "lean",
  "license": "ISC"
}

```

- We have two middlewares: `admin.js` 

```js
module.exports = async (req, res, next) => {
    if (!req.session.loggedin || req.session.permission != "administrator") {
        return res.status(401).send({message: "Not allowed"});
    }
    next();
};
```

and `auth.js`.

```js
module.exports = async (req, res, next) => {
    if (!req.session.loggedin) {
        return res.redirect("/panel/login");
    }
    next();
};
```

- We have a model called `users.js`:

```js
const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    username: { type: String, unique: true },
    password: String,
    permission: String,
});

const Users = mongoose.model("Users", userSchema);

module.exports = Users;
```

- we have two types of routes:
  - Generic:
    - `/`: redirects to `panel`
    - `/healthcheck`: uses auth middleware and receives a url. Uses a function called `check` from util/generic
    - `/healthcheck-dev`: uses auth middleware and receives a url. Uses a function called `getUrlStatusCode` from util/generic
  - Panel:
    - `/panel/register`: register a new account (Needs auth middleware)
    - `/panel/login`: Login into the account
    - `/panel/logout`: Logout user
    - `/panel`: its a dashboard with domains and ips presented as graphs, output from neo4j (Needs auth middleware)
    - `/panel/search`: search in a neo4j for a searchTerm and a field (Needs auth middleware)
    - `/panel/certificates`: get all certificates (Needs auth middleware)
    - `/panel/hosts`: get all hosts (Needs auth middleware)
    - `/panel/about`: about page (Needs auth middleware)
    - `/panel/management`: get all certificates (Needs admin middleware)
    - `/panel/management/addcert`: receives pem, pubkey and privkey then creates a certificate
    - `/panel/management/dl-certs`: get all certificates then create a zip with them.

Lets test the healthcheck endpoints:
- The `/healthcheck` endpoint is used to communicate with internal services and the filter bellow should be bypassed. But why do we need to call an internal service in this case? 
- hostname can't contain: `["localhost", "127", "0177", "000", "0x7", "0x0", "@0", "[::]", "0:0:0", "①②⑦"];`
- ports can't be: 1337 and 3000
- needs to have a port besides default ones such as 80 or 443.
- the path can't contain `healthcheck`
- For the `/healthcheck-dev` endpoint we are blocked by haproxy: `http-request deny if { path -i -m beg /healthcheck-dev }`
- **I think that if we can call `http://127.0.0.1/health-check?url= ; new_command ;` we can run commands into the target system** 

For the panel endpoints lets list the ones that we can interact with, besides register and login:
- `/panel/search`: accepts searchTerm and a field (auth middleware)
- `/panel/management/addcert` : accepts pem, pubkey and privkey (admin middleware)

`/panel/search` adds the field directly in the query:

```js
const searchQuery = `
      MATCH (h:Host)-[:HAS_CERTIFICATE]->(c:Certificate)
      WHERE c.${attributes[attribute]} = $value
      RETURN h.ipAddress AS ipAddress, COLLECT(c) AS certificates;
    `;
```

Can't do this challenge..