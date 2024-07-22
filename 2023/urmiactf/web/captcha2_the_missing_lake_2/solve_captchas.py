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