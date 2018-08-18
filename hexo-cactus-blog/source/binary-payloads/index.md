---
title: binary_payloads
date: 2018-05-05 16:06:46
---

## Process

### stdin
```sh
python -c 'print("\x90\x32\x45\x89")' | ./vuln
```

### stdin (Shell)
Let's say the address of a shell function is `0x89453290`. The below snippet passes that address via stdin but keeps stdin open afterwards using the `cat` program. With `cat`, you can interact with the shell after injecting the bytes.
```sh
(python -c 'print("\x90\x32\x45\x89")'; cat) | ./vuln
```

### stdin Using File
```sh
./vuln < myfile.txt
# Or this
cat myfile.txt | ./vuln
```

### Arguments
```sh
./vuln $(python -c 'print "\x41" * 36')
```

## GDB

### stdin
```sh
r < <(python -c 'print "\x41" * 36')
# Or this. Careful as this one might filter out NULL bytes
r <<< $(python -c 'print "\x41" * 36')
```

### stdin Using a File
```sh
r < myfile.txt
```

### Arguments
```sh
r $(python -c 'print "\x41" * 36')
```

## Remote Processes
Let's say `localhost:666` is running a vulnerable process that takes input via stdin.
```sh
python -c 'print "\xef\xbe\xad\xde"' | nc -vv localhost 666
```
The `-vv` flags just make the output very verbose.

## Convert stdin/stdout to Program Arguments
Some programs take their input from `argv` instead of stdin. However, it can be inconvenient to send large amounts of data to argv, so we can use a special program called `xargs` to help us. `xargs` takes whatever values that come into its stdin and uses them as arguments to the program given as its own argument.

Example:
The rm program on Unix systems receives the file names it should delete from argv. This could be cumbersome if you need to delete all files in a directory (let's pretend regex expansions and wildcards don't exist for this example). A potential solution is the following command.
```sh
# Deletes all non-hidden files in the current directory
ls | xargs rm
```

The stdout of ls is piped to the stdin of xargs, and xargs runs rm using that stdin as arguments to rm.
