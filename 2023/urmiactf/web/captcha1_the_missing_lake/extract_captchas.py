#!/usr/bin/python3
__author__ = "w0rth"

from bs4 import BeautifulSoup as BSHTML
import os, requests
import subprocess
import base64



def solve_captcha():
    s = requests.session()
    url = "https://captcha1.uctf.ir/"
    for i in range(300):
        r = s.get(url)
        html = r.text
        soup = BSHTML(html, "html.parser")
        print(soup.find_all("h4")[1])
        x = soup.find_all("img")[0]["src"].split(",")[1]
        open('captcha.png', 'wb').write( base64.decodebytes(bytes(x, 'utf-8')) )
        os.system('convert captcha.png -compress none -threshold 16% img.png')
        captcha = subprocess.run(['gocr', '-i', 'img.png'], stdout=subprocess.PIPE).stdout.strip()
        s.post(url, {'captcha': captcha.decode('utf-8')})
    print(s.get(url).text)
    

solve_captcha()