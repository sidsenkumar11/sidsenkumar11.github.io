---
title: stego
date: 2018-05-04 18:33:48
---

Here are some useful scripts and tools for steganography challenges.

## Stegsolve

Download [here](stegsolve.jar). Useful for looking at different shades of colors and more.

## Steghide

Steghide can be used to hide or send messages in images.
```
sudo apt-get -y install steghide
```

If you know data is steghide encrypted but need a password, you can brute force the password using this tool:
https://github.com/Va5c0/Steghide-Brute-Force-Tool

```
pip install progressbar
./steg_brute.py -b -d <dictionary> -f <file>
```

## Free File Camouflage

Free File Camouflage is another tool similar to steghide. It can be downloaded here as an executable.
http://www.myportablesoftware.com/free_file_camouflage.zip
