# Intro

Get your adrenaline pumping as you navigate the thrilling world of Crypto Web for Capture the Flag.
Flag format: PCTF{}

Author: @sau_12

# Challenge

it seems like it is a challenge to reverse the way the username and password are validated. Since all the validation is done in the frontend we will extract the javascript code and try to developed a setup to test. 

Username: adminjyu
password: aabcae

We have succeed in founding a valid username and password however there is no way we can submit this values.
We tried to put the username and password in a flag but they did not accept. An hint from the creator is that we need to find every combination possible and then brute force the form.