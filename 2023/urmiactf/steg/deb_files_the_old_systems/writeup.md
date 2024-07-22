# Tags
- Debian Packages

# Intro

Can you believe it? people still use linux? after the emerge of Evil E computers, nobody bothered to use linux systems. anyways, we got this file from database gaurds' pc, can you help us?

# Solution

We get a deb file which is a common extension for debian packages.
To extract it we use: `ar vx uctfdeb-0.0.1.deb`
Inside the data tar(`tar -xvzf data.tar.gz`) we have a executable with the following code: 

```
#!/usr/bin/env bash
if [ -f /tmp/UCTFDEB/dont-delete-me ]; then
        FLAG=`cat /tmp/UCTFDEB/dont-delete-me`
        if ! command -v curl > /dev/null; then
                echo 'Install curl and try again'
                exit 1
        else
                curl 127.0.0.1:7327 --header "flag: $FLAG"
else
        echo '404, there is no flag to be found'
    exit 1
```


Extracting the control tar(`tar -xvzf control.tar.gz`) we get two files:
- control
- postinst

Control file seems to have metadata about the debian package.
And the postinst file is a bash script that runs after installation. 
This file has the flag in it! 
Flag: `UCTF{c4n_p3n6u1n5_5urv1v3_1n_54l7_w473r}`