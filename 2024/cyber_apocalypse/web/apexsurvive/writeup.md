## Title

Apexsurvive

## Description

In a dystopian future, a group of Maze Runners faces a deadly labyrinth. To navigate it, they need vital intel on maze shifts and hidden passages. Your mission: hack into ApexSurvive, the black-market hub for survival gear, to obtain the key information. The Maze Runners' freedom depends on your skills. Time to infiltrate and hack the maze's lifeline. Good luck, hacker.

## Solution

It has a `mariadb` with two tables, `users` and `products`.
It has one user: 

```sql
INSERT INTO apexsurvive.users VALUES(
    1,
    'xclow3n@apexsurvive.htb',
    '$(genPass)',
    '',
    '',
    'Rajat Raghav',
    'xclow3n',
    'verified',
    'true',
    'true'
);
```

It uses `mailhog` version `v1.0.1`.
The flag is in `/root/flag.txt` but can be read by executing the binary: `/readflag`

There are three applications:
- A bot developed in python that has one endpoint `/visit`. It receives, `productID`, `email` and `password` has the arguments and visit the url `https://127.0.0.1:1337/challenge/` login with email and password and after having a session it searches for a product in `https://127.0.0.1:1337/challenge/product/{productID}`.
The problem is that the only port that is exposed is 1337 and the bot is running on the port 8082 internally.

- An email app developed in javascript that has two endpoints `/email` and `/email/deleteall`. `/email` endpoint gets a list of 10 emails and retrieve the ones that the `receive` is `test@email.htb`. `/email/deleteall` in the other end deletes every email.

- Finally we have a challenge app. This app is developed in python and uses **wsgi** has the gateway. We have three blueprints each one with multiple endpoints, `/challenge`, `/challenge/api` and `/`.
    - `/challenge`:
        - `/verify`: receives a token that is used to verify the email
        - `/settings`: show user settings (Needs auth)
        - `/home`: shows home page to the user (Needs auth and verification)
        - `/product/<productID>`: receives `productid` shows the product page (Needs auth and verification)
        - `/product/addProduct`: shows add product page (Needs auth, verification and internal)
        - `/admin/contracts`: shows contracts (Needs auth, verification, internal and admin)
        - `/logout`: logout of the session
        - `/external`: receives a parameter called `url` and redirects to that page.
    - `/`: Only has one endpoint which is `/` and provides information about the challenge
    - `/challenge/api`:
        - `/login`: receives `email` and `password` ans logins
        - `/register`: receives `email` and `password` and logins
        - `/profile`: receives `email`, `fullName` and `username`, this endpoint changes user info. It has a error message `return response('Why are you trying to break it? Something went wrong!')`. Maybe its a entrypoint.
        - `/sendVerification`: endpoint to verify the email
        - `/report`: receives `id` of a product and will use the bot and visit the product page (Needs auth and verify)
        - `/addItem`: receive `name`, `price`, `imageURL`, `description`, `note`, `seller` and add the item to the db (Needs auth, verify and internal)
        - `/addContract`: receive `name` and a file `file`, save it in `/tmp/temporaryUpload` and check if its a pdf. It has an interesting error message: `('Invalid PDF! what are you trying to do?')`



raneto3180@dovesilo.com