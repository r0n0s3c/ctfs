## Title

Bean Cafe

## Description

This cool cafe offers a super secret menu! But it's being guarded by some AI detection systems. Hopefully we can get through it to try the coffee...

Note: Automated tools like sqlmap and dirbuster are not allowed (and will not be helpful anyway).

## Solution

It seems like when we put an image of a bean plant it recognizes it but when comparing images it may use a weak hash algorithm like md5. 
If we can generate a collision with a rust leafs image we can pass the challenge.

I found two images with the same md5, one is a plane which it identifies as the healthy leaf and other is a shipwreck which it identifies as rust leafs.
This challenge has two weaknesses, the first is that it only have two options when identifying images and the other is the comparison algorithm which is as hash algorithm very easy to find collisions.

Flag: `wctf{new_ai_old_algorithm}`