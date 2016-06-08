import sys

def egcd(a, b): #inverse mod function (its not built in :O)
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m): #inverse mod function
    g, x, y = egcd(a, m)
    if g != 1:
        return -1
    else:
        return x % m

c = int("ac470f7350ea67d7a0696",16)
p =  1398023584459
q =  29065965967667

e = 2 # start guessing e at 2

while 1: #loops infinitely until flag is found
    d = modinv(e,(p-1)*(q-1)) #uses inverse mod
    if(d!=-1):
        answer = (hex(pow(c,d,p*q))) #turns into hex after powmod
        answer = answer[2:-1]
        if(len(answer)%2==1):
            answer = '0' + answer
        xyzwhatever = answer.decode("hex") #turns hex to ascii
        if("rsa" in xyzwhatever.lower()): #prints flag if "rsa" is in it (.lower() prevents case sensitivity)
            print(e) #prints public exponent used
            print xyzwhatever #prints possible flags
    e = e + 1