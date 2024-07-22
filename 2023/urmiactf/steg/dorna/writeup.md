# Tags
- Steghide

# Intro

I'm hiding somewhere. Find me if you can!!

if you need a password anywhere use this "urumdorn4"

# Solution

We use steghide to extract the files inside the image: `steghide extract -sf dorna.jpg` with the password specified in the introduction.
We get the flag encoded in base64: `uctf{ZG9ybmFfbGFyX3lvdmFzaQ==} `
flag: `uctf{dorna_lar_yovasi}`