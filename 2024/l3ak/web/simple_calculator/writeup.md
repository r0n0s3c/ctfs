## Title 

Simple Calculator

## Description

Unveil PHP Secrets.

Author: S1mple


## Solution

This is a white box challenge where we have a main endpoint that accepts a parameter *formula* and uses the eval function to calculate the result. However the input is directly put into it if it passes the following filters:

`if (strlen($formula) >= 150 || preg_match('/[a-z\'"]+/i', $formula))`

- The string needs to have less then 150 characters.
- Regex has a Global pattern flag insensitive and match each letter from a to z, ' and ".

This are some examples:
- https://ironhackers.es/en/tutoriales/saltandose-waf-ejecucion-de-codigo-php-sin-letras/
- https://securityonline.info/bypass-waf-php-webshell-without-numbers-letters/
- https://ctf-wiki.org/web/php/php/#preg_match-code-execution
- https://github.com/m3ssap0/CTF-Writeups/blob/b83e31b155a13d642e527968a9375c295c6a6977/Inferno%20CTF%202019/Dank%20PHP/README.md
- https://github.com/m3ssap0/CTF-Writeups/blob/master/ASIS%20CTF%20Quals%202020/Web%20Warm-up/README.md

Basically the idea is using octal, like:
l -> 108(ASCII) -> 154(Octal)
s -> 115(ASCII) -> 163(Octal)

Together it makes \154\163, the final payload is: 
```http
GET /?formula=`\154\163`
```

