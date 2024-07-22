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