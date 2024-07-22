# Tags
- Autopsy
- VHD
- Disk Analysis

# Intro

Explore the available streams and consider the different types of data that can be associated with a single filename. Good luck!

# Solution

Once we extract the challenge zip we get a file with the extension vhd. This extension refers to a virtual disk. The next step is to mount the volume and analyse it.

## Mount volume
We can do this by mounting it in our machine:

```
sudo apt-get install libguestfs-tools
sudo guestfish --ro -a stream-ctf.vhd
run
list-filesystems
mkdir ./stream_ctf
sudo guestmount -a  stream-ctf.vhd -m /dev/sda1 --ro ./stream_ctf
sudo -i
```

Once we have mounted the disk to a directory we change to root user and access it. We found a flag.zip that can't be unziped. 
Using strings command we get `password:Atoosa`

To unmount the disk we run the following commands: `sudo guestunmount ./stream_ctf`


## autopsy
Or using autopsy:

```
sudo apt-get update && sudo apt-get install autopsy && sudo autopsy &
```

With autopsy we get flag.zip and flag.zip:lookbehind.
Flag.zip has the same string we found with the mounting technique `password:Atoosa`
flag.zip:lookbehind has the string uctf_flag.txt when looking at the content with autopsy. This means that it may contain the flag inside it.

When we export the flag.zip:lookbehind, change the name to flag.zip and extracting the content(`unzip flag.zip`), 
we get the following answer: `skipping: uctf_flag.txt           unsupported compression method 99`
Looking at the error(https://access.redhat.com/solutions/59700) we found out that its root comes from a AES error.
The file is encrypted with AES which is a asymmetric encryption. Using the file manager UI, in my case caja, when we try to open it we are prompt for a password.
Using `Atoosa` we get the flag: `uctf{St. Mary Church}`






