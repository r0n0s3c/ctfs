# Tags
- Captcha Bypass

# Intro

Our low-budget human captcha solvers have gone missing. We need you to help us crack our way into the city's old database, where did the lake go? We gotta find out!

# Solution

This challenge was a mroe programming challenge where we saved the images and used gocr to get the text from the image.
We used beatifulsoup to extract the base64 image, decode it, write it to a file and used gocr to get the text from it. Doing this 300 times we get the flag. 
flag:  UCTF{7h3_m1551n6_l4k3}