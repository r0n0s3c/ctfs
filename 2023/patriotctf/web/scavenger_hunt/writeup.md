# Intro

Can you find all the hidden pieces of the flag?
Author: @txnner

# Challenge

We are presented with a challenge of gathering 5 different flags that will make the flag of the challenge.
The first they gave us in the first page we access: `Flag 1/5 - PCTF{Hunt`
Flag 2 is in a comment in the html source code: `Flag 2/5 - 3r5_4n`
Openning the dev console we get the fourth flag: `Flag 4/5 - R5_e49` and get a warning about a fiveth flag: `Cookie “Flag 5/5” does not have a proper “SameSite” attribute value.`. Looking at the cookie we ge the fiveth piece: `e4a541}`
However we need the third flag to finish the challenge, after some time, we remember that some websites have robots.txt. Looking there, we found the third flag: `Flag 3/5 - D_g4tH3`


FLAG: `PCTF{Hunt3r5_4nD_g4tH3R5_e49e4a541}`