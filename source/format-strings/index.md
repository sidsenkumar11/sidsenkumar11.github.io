---
title: format-strings
date: 2018-05-05 16:16:45
---

The best article I've found explaining format string attacks via an example is the following website: [http://codearcana.com/posts/2013/05/02/introduction-to-format-string-exploits.html](http://codearcana.com/posts/2013/05/02/introduction-to-format-string-exploits.html)

## Print the Stack
```sh
# prints 8 hex digits to represent each argument to printf.
'AAAA' + '%08x ' * 9 + '%08x'
```
You can use this to enumerate values on the stack and eventually find the location of the printf string itself. By continuing until you see '41414141', you will know you've found the string holding the input passed to the printf function since '41414141' is the 4 A's we passed in at the beginning of the printf string.

## Direct Parameter Access
Access the nth argument to printf (whether n arguments were actually passed in or not!)
```sh
%<arg n>$<format>
```
Ex. `printf("%3$d", 1, 2, 3)` prints '3'.

## Writing Data to Arbitrary Memory
The "%n" modifier writes the number of bytes printed to a specified address.
```sh
printf('Hello!', &n); # n will contain 6 after this executes.
```
As shown before, we can locate the beginning of the printf string on the stack. After that, we can swap the last '%08x' with a '%n' and swap the 'AAAA' with an address that you want to write to - allowing us to write to arbitrary memory locations.

However, we still need to control exactly what we write. The only value we can write is how much data has been printed out. Unfortunately, we need to print a lot of characters if we want to write large values like addresses, which seems infeasible at first. Usually the printf buffer won't be able to handle thousands of characters being thrown at it.

So, instead of writing the whole address at once, we split our write into two chunks like below. First we write to the upper two bytes of the target address, then we write to the lower two bytes of the target address.

```python
# Let's say we want to replace the GOT entry of 'exit' with the address of a
# function called 'printFlag'. &printFlag = 0x804872b
got_addr = e.got['exit']
payload = p32(got_addr + 2) + p32(got_addr)
payload += "%2036x%26$hn"
payload += "%32551x%27$hn"
```

First, we specify the address `got_addr + 2` and `got_addr`. When the format string finishes reading its fake arguments (everything on the stack until the format string itself), it will interpret these two arguments as addresses that will be written to by a `%n`.

Next, we specify the portion of the format string that will skip past all the arguments to printf (i.e. everything on the stack until the format string itself).

Dissected:
```plain
%2036x - print 2036 bytes. This (or some offset of it) is the value we want to write to the upper half of got_addr + 2.
%26    - write to the 26th argument of the printf function (this is how we skip all the fake arguments to printf on the stack).
$hn    - write only two bytes.
```
