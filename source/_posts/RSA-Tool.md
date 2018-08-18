---
title: RSA Tool
author: Siddarth Senthilkumar
comments: true
date: 2018-01-18 10:21:38
tags:
- RSA
- CTF
- Cryptography
---

Many CTF competitions come with some kind of RSA cryptography challenge. These challenges vary in difficulty but usually use the same textbook RSA calculations. To speed up my solve times, I've created some simple scripts to help solve the most common RSA CTF challenges. Many of them are snippets I've found online and adapted to work with my utilities.

## Installation
Download the folder linked below and then install dependencies.

```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

`run.py` is the runner program. You can use all the functions in `attack_functions.py` and `pem_utilities.py`.

1. `attack_functions` contains functions that perform numerical attacks against RSA and provides some basic utilities, such as converting integers to ASCII text.

2. `pem_utilities` contains functions that make it easier to work with PEM files or files that have been encrypted using openssl.

### Online Factorization
```python
from attack_functions import *
n = 28951349384423043218983050540262097638996616109955577558902029524079760750158684923657109854846122191130360573015845720440777033197971499589196069264739625195198815368193977724349036642939995805368573744328447244579642526857449768268753834475805477560338041038092683043149578111742677114084484145949297041276137332636132506885331222738476811693140185976545715701414240079516065192740228585267852582046443608026161708941442363792964096239980728739084441464942853065825759132585180831506997153733610602370711588167486294114891207572485931146617054305640945613324997820264892045579903140276482436750764783137418434959509
e = 65537
c = 4531850464036745618300770366164614386495084945985129111541252641569745463086472656370005978297267807299415858324820149933137259813719550825795569865301790252501254180057121806754411506817019631341846094836070057184169015820234429382145019281935017707994070217705460907511942438972962653164287761695982230728969508370400854478181107445003385579261993625770566932506870421547033934140554009090766102575218045185956824020910463996496543098753308927618692783836021742365910050093343747616861660744940014683025321538719970946739880943167282065095406465354971096477229669290277771547093476011147370441338501427786766482964

p, q = factordb(n)
print ascii(given_p_q(c, e, n, p, q))
```

### Working with PEMs
```python
from attack_functions import *
from pem_utilities import *

import glob

# Get all file names that end with .key or .enc (if necessary)
# key_files = glob.glob("./*.key")
# cipher_files = glob.glob("./*.enc")

ciphertext_fname = "flag.enc"


# Crack the key, get factors
p = 0x00d1555acceb95d63216845cd1de64d6cc5ba6a878e9efb2d453b2fbd3c571a8993f804d449527f11e2c7d2f53e25afce5f99d38c5103772271be9ebaee09db41f
q = 0x00c93ceed82db2840160c52ed77b346ace00ff0b04a82f28f4ffa42c47362ec34bf885e4f8ef4304363addd5cee79f8d6cfead8b591d5167fd6168641a9fd6600d
n = p * q
phi_n = (p-1) * (q-1)

e = 65537
priv_key = gen_private_key_p_q(n, long(e), p, q)

# Decrypt the ciphertext file
# decrypt_file(ciphertext_fname, priv_key)

# If you desire more accuracy, write the private key to a file then decrypt using openssl
# openssl rsautl -decrypt -inkey private.pem < ctfexample-text.txt
# Write PEM to file
with open ("private.pem", "w") as prv_file:
    prv_file.write("{}".format(priv_key.exportKey()))
```

## Notes

1. Small public modulus n - use https://factordb.com/index.php to find p and q.
2. Given multiple keys - see if any of the keys have common factors using the Euclidean Algorithm.
```python
import fractions
print(fractions.gcd(a, b))
```
3. p and q are close to each other - use YAFU or https://www.alpertron.com.ar/ECM.HTM
4. Two ciphertexts use the same modulus n but different exponents e - use: same_modulus.py
5. Small p or q - use YAFU or https://www.alpertron.com.ar/ECM.HTM
6. Large e or d - Wiener's attack. Use attackrsa tool.
7. Same m and e for multiple messages - Hastad's Broadcast Attack. Use attackrsa tool.
8. If num_ciphertexts >= e then you can use Chinese Remainder Theorem to calculate the message (but gcd of all n's must be 1 - if the gcd between any two n's is not 1, then you can just find a common factor between them).

## External Utility Notes
Here are some commands to transform and work with keys.

Given n and d, print e, p, q.

```sh
python rsatool.py -n 13826123222358393307 -d 9793706120266356337
```

Given n and d, print PEM format.

```sh
# cd rsatool
python rsatool.py -f PEM -o key_file.pem -n 13826123222358393307 -d 9793706120266356337
```

Given p and q, print DER format.

```sh
# cd rsatool
python rsatool.py -f DER -o key_file.der -p 4184799299 -q 3303891593
```

Factorize with YAFU.
```sh
./yafu "factor(0xD8E24C12B7B99EFE0A9BC04A6A3DF58A2A944269B492B7376DF129023F2061B9)" -threads 5
```
