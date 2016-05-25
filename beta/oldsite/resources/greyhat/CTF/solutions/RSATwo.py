def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

# Given:
c = 679293973228377073
e = 17
n = 944871836856449473

# From WolframAlpha:
p = 961748941
q = 982451653

totientN = (p - 1) * (q - 1)
d = modinv(e, totientN)

plaintext = pow(c, d, n)

# Convert to ASCII
plaintext = hex(plaintext)[2:len(hex(plaintext)) - 1]
plaintext = plaintext.decode('hex')

# Print result
print(plaintext)