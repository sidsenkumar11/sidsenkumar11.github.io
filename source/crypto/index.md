---
title: crypto
date: 2018-05-04 18:17:13
---

## Caesar Cipher
Caesar Cipher-encryption just involves shifting each alphabetic letter by some number.
Automatically guess shift number: [https://www.xarg.org/tools/caesar-cipher/](https://www.xarg.org/tools/caesar-cipher/)
Print all shifts: [caesar_all.py](scripts/caesar_all.py)

## Substitution Cipher
Substitution ciphers substitute each letter with another letter. They can be cracked by frequency analysis.
Guess cipher: [http://quipqiup.com/index.php](http://quipqiup.com/index.php)
View n-grams to help guess letters: subst.py and [https://ehsandev.com/pico2014/cryptography/substitution.html](https://ehsandev.com/pico2014/cryptography/substitution.html)

## Block Ciphers
Simple XOR CBC key finding script: [bricks_of_gold_csaw_2015.py](scripts/bricks_of_gold_csaw_2015.py)

## RSA

### Setup
Use this script to install a few useful utilities for working with RSA problems. You will need git, python, pip, and virtualenv already installed on your system.
[install_rsa.sh](scripts/install_rsa.sh)

### General RSA Attack Notes

1. Small public modulus n - use https://factordb.com/index.php to find p and q.
2. Given multiple keys - see if any of the keys have common factors using the Euclidean Algorithm.

```python
    import fractions
    print(fractions.gcd(a, b))
```

3. p and q are close to each other - use YAFU or https://www.alpertron.com.ar/ECM.HTM
4. Two ciphertexts use the same modulus n but different exponents e - use: [same_modulus.py](scripts/same_modulus.py)
5. Small p or q - use YAFU or https://www.alpertron.com.ar/ECM.HTM
6. Large e or d - Wiener's attack. Use attackrsa tool.
7. Same m and e for multiple messages - Hastad's Broadcast Attack. Use attackrsa tool.
8. If num_ciphertexts >= e then you can use Chinese Remainder Theorem to calculate the message (but gcd of all n's must be 1 - if the gcd between any two n's is not 1, then you can just find a common factor between them).
9. If c < n, just take the eth root of c to get the plaintext.

### Basic RSA Decryption
If you can easily find p and q or d, then you can use this script to decrypt a ciphertext to ASCII.
[decrypt_rsa.py](scripts/decrypt_rsa.py)

### Commands
Here are some commands to transform and work with keys.

#### Given n and d, print e, p, q.
```
python rsatool.py -n 13826123222358393307 -d 9793706120266356337
```

#### Given n and d, print PEM format.
```
# cd rsatool
python rsatool.py -f PEM -o key_file.pem -n 13826123222358393307 -d 9793706120266356337
```

#### Given p and q, print DER format.
```
# cd rsatool
python rsatool.py -f DER -o key_file.der -p 4184799299 -q 3303891593
```

#### Factorize with YAFU.
```
./yafu "factor(0xD8E24C12B7B99EFE0A9BC04A6A3DF58A2A944269B492B7376DF129023F2061B9)" -threads 5
```
