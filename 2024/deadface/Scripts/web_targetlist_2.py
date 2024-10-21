import requests

def xor_strings(input_str, key):
    return ''.join([chr(ord(input_str[i]) ^ ord(key[i % len(key)])) for i in range(len(input_str))])


xor_key = "V}bD}e"
fake_input = "f620f126271"
value = "0\"OR\"1"
# input = xor_strings(fake_input, value) # Dy`W~y`
#print(input)
input = xor_strings(xor_key, value) 
print(input)
#resp = requests.get(f"http://targetlist.deadface.io:3001/pages?page={input}")
#print(resp.text)