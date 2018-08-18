---
title: Pwn Path
author: Siddarth Senthilkumar
date: 2018-04-30 22:39:53
comments: true
tags:
- Binary Exploitation
- Reverse Engineering
---


I've been learning the basics of reverse engineering and binary exploitation for almost a year now. While I don't consider myself an expert, I've learned more than I thought possible for myself in a short time. One of the problems I've had was finding good problem sets designed for learning with increasing steps of difficulty. So, I'm creating my own series of challenges curated from various sources that provide a good progression of difficulty for anyone interested in binary exploitation.

Note that I give a solution description for each challenge. These challenges are not meant for you to frustrate yourself with finding vulnerabilities - you'll eventually be able to do that after playing with a binary and it'll just waste your time while you're learning. Here, anyone who wants to learn a specific exploitation technique can refer to a sample problem and learn by doing.

## Level 0: Reverse Engineering with IOLI
The IOLI crackmes are the best place to start if you have zero experience with looking at binaries. A crackme is a challenge in which you are given a compiled program that requires a password. Usually, we aren't given the program source code so we have to figure out what the necessary input is from the assembly instructions in the binary.

In each of the IOLI crackmes, the binary will ask the user for a password and then print whether or not that password was correct. Our goal is to reverse engineer the correct passwords and gain access. Personally, I only think it's worth doing these challenges until crackme0x07 since the solutions can get repetitive.

Challenge | Description
--- | ---
crackme0x00a | Hardcoded string comparison
crackme0x00b | Interesting hardcoded string comparison
crackme0x01 | Hardcoded integer comparison
crackme0x02 | Using GDB to avoid long computations
crackme0x03 | String obfuscation and educated guessing
crackme0x04 | Operations on string characters
crackme0x05 | Bitwise operations
crackme0x06 | Environment variables
crackme0x07 | Stripped symbols

Download: [crackmes.tar.gz](challenges/crackmes.tar.gz)

Original: [challenges.zip](http://security.cs.rpi.edu/courses/binexp-spring2015/lectures/2/challenges.zip)

## Level 1: Buffer Overflows
Now that you have a basic understanding of assembly language, static analysis, and debugging, you are ready to learn about buffer overflows. In a buffer overflow, you provide more data to a program than can fit in a specified buffer - causing the program to overwrite important data on the stack such as local variables and saved instruction pointers.

Challenge | Description
--- | ---
MBE Lab 2C | Controlling stack variables
MBE Lab 2B | Calling functions with arguments
MBE Lab 2A | Call a function in a weird way

These challenges and many of the future ones come from RPISEC's Modern Binary Exploitation course. I highly recommend you go through their slides prior to attempting these challenges. They give you detailed explanations on how the exploits work and even provide useful commands.

[PDFs of MBE Lectures](https://github.com/RPISEC/MBE/releases/download/v1.1_release/MBE_lectures.tar.gz)

[Compiled MBE Binaries](https://github.com/RPISEC/MBE/releases/download/v1.1_release/MBE_release.tar.gz)

## Level 2: Shellcoding
In the previous challenges, there was always a "shell" function that you just could call which would give you a shell. However, there's almost never a random shell function lying around in a real program.

Shellcoding is the art of writing instructions you want to execute on the stack, and then overwriting the return address pointer to point to the shellcode you wrote. Note that shellcode doesn't necessarily need to spawn a shell; shellcode refers to any executable code that the user provided - even if it's as simple as printing "Hello World".

MBE Lab 3C | Returning to shellcode
MBE Lab 3B | Write shellcode that doesn't spawn a shell
MBE Lab 3A | Write non-contiguous shellcode (limited space)

## Level 3: ROP Emporium
These days, shellcoding problems occur less frequently. This is because of a protection built into binaries called "NX bit" or "W^X". NX stands for no-execute and refers to the fact that that writeable sections of memory must also be non-executable. This way, even if an attacker gains access to the instruction pointer, they can't redirect execution to code that they wrote since the section that they wrote to will be non-executable.

However, attackers have come up with ways to bypass this protection in the form of return-oriented programming, or ROP. We still overflow and control the instruction pointer, but now we execute chains of instructions that already exist in the binary's code or in imported code.

The majority of these challenges come from ROP Emporium, which I found to be an excellent set of challenges for learning ROP chaining. For more information about each challenge, visit the ROP Emporium website linked below. It will tell you what kind of exploit you need to do and give you hints (which will save you the trouble of having to reverse engineer the problem before beginning the exploit). You should make sure to do both the 32-bit and 64-bit challenges since there are interesting nuances between the architectures that will affect your ROP chains.

Challenge | Description
--- | ---
ret2win | Controlling $eip
split | Calling functions with arguments, both found in the binary
callme | Calling exteral functions using the PLT
write4 | Pass arbitrary arguments to functions that expect pointers by writing to .data
fluff | Using more difficult gadget patterns to construct ROP chains
pivot | Stack pivoting and adding offsets to get to a new function in libc file. You may want to do this after finishing Level 4.

Original: [ROP Emporium](https://ropemporium.com/)

## Level 4: Format Strings
We've been doing relatively simple overflows until now - we just happen to overwrite data on the stack because the program read in more input than it should. What other ways can we control the instruction pointer? Format strings! Format strings are often used with functions like `printf` to interpret sequences of bytes as integers, or characters, or even pointers. `printf` doesn't get passed in the number arguments to it - so if a format string was read as `%x%x%x` and the user didn't provide three numbers, then `printf` just starts reading up the stack and printing out three numbers since it'll think that those were the arguments to it. You can see the problems that this might cause. There is also a special format string, `%n`, which will allow you to write to arbitrary regions of memory.

For more information, read the MBE slides on format strings and check out this excellent [tutorial]( http://codearcana.com/posts/2013/05/02/introduction-to-format-string-exploits.html).

Format string challenges are important but can be a little tricky. You might argue that they are less complicated than ROP challenges, but I think it helps to learn the stack well and understand what memory sections are writeable before learning to exploit format string vulnerabilities. The challenges in this section are from angstromCTF 2018 and include the source code for each binary.

Challenge | Description
--- | ---
Number Guess | Leak private local variables
Letter | Use `%n` to overwrite data in arbitrary memory locations

Download: [format_strings.tar.gz](challenges/format_strings.tar.gz)

## Level 5: Gadgets in Shared Objects & Defeating ASLR
Until now with the ROP Emporium challenges, we've been solely using gadgets found in the binary that we're running. However, you can also use gadgets found in the linked shared object files such as libc.so. In fact, this will usually make your exploits easier because there are so many gadgets in the libc shared object.

There is a catch though - it is slightly more work to ROP chain using the shared objects. Shared objects are compiled with a protection known as PIE, which stands for Position Independent Execution. If you look at a shared object file in a disassembler, you'll see that each instruction's address is something like `0x00000xxx`. This indicates that the .so file was compiled with PIE. When the shared object is loaded and run, the operating system chooses a random base address and all the address in the shared object are referenced by `random_base + 0x00000xxx`. This is known as ASLR.

When an operating system has ASLR enabled and a binary is compiled with PIE, you can't just jump to a fixed gadget addresses found in the binary and expect the jump to work. This is because the shared object's base address will be randomized during the load time of the library. So how can we defeat this protectoin?

Well, the offsets within the library remain the same between runs even if the base addresses are different. Therefore, if you know the full address of any function, you can use the offsets in the .so file to calculate the address of any other function in that shared object. Getting the address of any function in the PLT is known as a leak.

The reason we haven't had to deal with ASLR in the ROP Emporium challenges (even though ASLR was enabled!) is that we only looked for gadgets in the binary itself. Those binaries were not compiled with PIE (position independent execution), so ASLR didn't affect them. Shared objects are always compiled with PIE, so ASLR affects them. If we had compiled the binaries in ROP Emporium with PIE, then you'd have to do the same kind of leak as discussed before to get the addresses of the gadgets before being able to jump to them. After leaking, the process is the same as usual for constructing a ROP chain.

Challenge | Description
--- | ---
ROPU | Leak an address using puts, then jump to a target from one-gadget.
Ropasaurus Rex | Another leak but slightly more difficult (uses read() / write())
scv | Leak a stack canary using format strings

## Solutions
I'm working on creating a set of solutions for each of these challenges. Once it's done, I'll post it here.
