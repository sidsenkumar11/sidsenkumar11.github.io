---
title: gdb-tips
date: 2018-05-05 16:08:24
---

## PEDA Patterns
In pwn problems, we often need to find the size of a buffer that we're going to overflow. Instead of guessing the buffer offset until we reach something interesting, we can use patterns in the GDB extension PEDA. Note that the patterns given should be stripped of leading and trailing quotation marks before being used.

```sh
pattern create 1035
```

To search for the pattern in the program context, you can simply run the following.
```sh
pattern search
```

#### 64-bit Note
In 64-bit binaries, the binary doesn't continue running before it segfaults - i.e. the binary segfaults right before it would have obtained an invalid $rip.

Therefore, we wouldn't be able to use `pattern seach` to see where the offset is and must manually check the stack pattern bytes that would have been popped into $rip. After copying the 8 bytes that would have gone into $rip, we can use the following to see the offset.
```sh
pattern offset <pattern_bytes>
```

## Attaching GDB to a Process
When you run a binary in GDB, the binary runs with ASLR off by default and the number of environment variables is different from if you had run the raw binary.

For this reason, it's often more useful to attach GDB to a running process than running GDB from the start.

In one terminal, run the binary until it hits a point where the user has to enter input - otherwise the process might terminate before we even have time to attach to it.
```sh
./vuln
```

In another terminal, attach with GDB like this.
```sh
sudo gdb vuln `pidof vuln`
# Or
sudo gdb -p `pidof vuln`
```

## Jumping to an Address
You can jump to a specific address at any time during a binary's execution using GDB.
```sh
jump *address
```

## Python Interpreter
This is a small one but easy to forget - there's a built in Python interpreter in GDB that you can use while debugging, so you don't have to exit GDB or open a new window! I haven't played with it too much but it might default to Python 3 (I couldn't import modules like `pwn`). However, it works in a pinch when you need to convert hex digits to integers or vice-versa.

```sh
gdb-peda$ pi
>>> 0xdeadbeef
3735928559
>>>
```
