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

def decrypt(c, e, n, d=0, p=0, q=0):

    # If p and q are given, calculate d
    if d == 0 and p != 0 and q != 0:
        totientN = (p - 1) * (q - 1)
        d = modinv(e, totientN)

    plaintext = pow(c, d, n)
    return plaintext

def display_plain_as_ascii(plaintext):
    plaintext = hex(plaintext)[2:len(hex(plaintext)) - 1]
    plaintext = plaintext.decode('hex')
    return plaintext

if __name__ == "__main__":

    # Given - change these:
    c = 679293973228377073
    e = 17
    n = 944871836856449473

    # Enter either d or (p and q):
    d = 166742088513926273
    p = 0
    q = 0

    # Print result
    plaintext = decrypt(c, e, n, d, p, q)
    print(display_plain_as_ascii(plaintext))
