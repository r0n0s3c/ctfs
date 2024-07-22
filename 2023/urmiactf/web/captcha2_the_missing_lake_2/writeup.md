# Intro

Sorry for bothering you again! We forgot to retrieve some valuable assets the last time. They have changed their captcha system, I think they know that we know about OCRs :)

# Domain

Since there was not domain in the challenge I start to looking around the previous domain: https://captcha1.uctf.ir/
However we didn't found nothing. So we tried https://captcha2.uctf.ir/ and we got what seems the challenge 2 of captcha.

# Solution

This time we get animal image. In this captcha we get a combination of two animal images and we need to add both using the following format: `animal1-animal2`
Since animals probably are less than a combination of numbers and letters from the previous challenge, lets make some requests to the page to look what animals can we have. The response contains two jpeg images. We will make 200 requests and store every image in a file. Then we will categorize each image and make a dictionary in python to further solve the captcha. This all in the assumption that we have a low number of animals.

```python
#!/usr/bin/python3
__author__ = "w0rth"

from bs4 import BeautifulSoup as BSHTML
import requests

def store_images(x):
    file = open("images.txt", "w+")
    for i in x:
        file.write(i + "\n")
    file.close()
def get_image():
    
    s = requests.session()
    url = "https://captcha2.uctf.ir/"
    image_list= []
    for i in range(200):
        r = s.get(url)
        html = r.text
        soup = BSHTML(html, "html.parser")
        for image in soup.find_all("img"):
            if image["src"] not in image_list:
                image_list.append(image["src"])
    return image_list

x = get_image()
store_images(x)

```

After making 200 requests we get 11 different images. Bellow is the final list:

```
6D0EBBBDCE32474DB8141D23D2C01BD9628D6E5F.jpeg rabbit
09F5EDEB4F5B2A4E4364F6B654682C6758A3FA16.jpeg bear
E49512524F47B4138D850C9D9D85972927281DA0.jpeg dog
FF0F0A8B656F0B44C26933ACD2E367B6C1211290.jpeg fox
73335C221018B95C013FF3F074BD9E8550E8D48E.jpeg penguin
091B5035885C00170FEC9ECF24224933E3DE3FCC.jpeg horse
9E05E6832CAFFCA519722B608570B8FF4935B94D.jpeg mouse
9D989E8D27DC9E0EC3389FC855F142C3D40F0C50.jpeg cat
148627088915C721CCEBB4C611B859031037E6AD.jpeg snake
5ECE240085B9AD85B64896082E3761C54EF581DE.jpeg duck
C29E4D9C8824409119EAA8BA182051B89121E663.jpeg eagle
```

```python
#!/usr/bin/python3
__author__ = "w0rth"

from bs4 import BeautifulSoup as BSHTML
import requests

animal = {
    "6D0EBBBDCE32474DB8141D23D2C01BD9628D6E5F.jpeg": "rabbit",
    "09F5EDEB4F5B2A4E4364F6B654682C6758A3FA16.jpeg": "bear",
    "E49512524F47B4138D850C9D9D85972927281DA0.jpeg": "dog",
    "FF0F0A8B656F0B44C26933ACD2E367B6C1211290.jpeg": "fox",
    "73335C221018B95C013FF3F074BD9E8550E8D48E.jpeg": "penguin",
    "091B5035885C00170FEC9ECF24224933E3DE3FCC.jpeg": "horse",
    "9E05E6832CAFFCA519722B608570B8FF4935B94D.jpeg": "mouse",
    "9D989E8D27DC9E0EC3389FC855F142C3D40F0C50.jpeg": "cat",
    "148627088915C721CCEBB4C611B859031037E6AD.jpeg": "snake",
    "5ECE240085B9AD85B64896082E3761C54EF581DE.jpeg": "duck",
    "C29E4D9C8824409119EAA8BA182051B89121E663.jpeg": "eagle"
}


def solve_captcha():
    s = requests.session()
    url = "https://captcha2.uctf.ir/"
    for i in range(100):
        r = s.get(url)
        html = r.text
        soup = BSHTML(html, "html.parser")
        captcha = animal[soup.find_all("img")[0]["src"]] + "-" + animal[soup.find_all("img")[1]["src"]]
        print(captcha)
        myobj = {'captcha': captcha}
        s.post(url, data=myobj)
    print(s.get(url).text)
    

solve_captcha()
```



You have done it! there you go UCTF{Arm3n1an_m0uflon}