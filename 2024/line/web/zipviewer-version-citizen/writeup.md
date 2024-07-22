## Zipviewer Version Citizen

We have four different endpoints:
- `/web/{username}`: We get a vapor session that is generated using the username and random UUID and we get the bellow message:

```
{"message":"Welcome, myname","status":200}
```

- `/viewer`: 
  - Endpoint to see our files, upload and download too.
  - The link internally for the files is stored using: `/Upload/GenerateSHA256(username + uuid + SALT)`(We dont know the salt nor the UUID)

- `/upload`:
  -  It submits a zip file to `/Upload/GenerateSHA256(username + uuid + SALT) + .zip`
  -  It seems like we can't control any input since the only thing that is used is generated

- `download`:
  -   