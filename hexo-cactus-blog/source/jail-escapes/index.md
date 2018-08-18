---
title: jail-escapes
date: 2018-08-14 07:55:46
---

# Python Interpreters

## Useful Knowledge

There's a lot you can do within an interpreter even without direct access to source.

1. `dir()` will list out all the available names inside the current space. You can also use `dir()` on a function to see what attributes and properties the function has.

2. `func_name.func_code` has a ton of useful properties to get information about the function. Among the most useful:
- `func_name.func_code.argcount` - Self-explanatory
- `func_name.func_code.co_code` - Gives you the bytecode representing the function.
- `func_name.func_code.co_consts` - Constant numbers and strings present inside the function.
- `func_name.func_code.co_varnames` - Names of variables inside the function.

## Eval to String when Alphanumeric Characters Disallowed

I first came across this problem during TJCTF 2018, "Mirror Mirror".
We were dropped into an REPL with the knowledge that there was a get_flag function.
Here is what the code looked like:
```python
super_secret_string = 'this_is_the_super_secret_string'
def get_flag(input):
	if input.isalnum() or '_' in input:
		return "Character not allowed"

    if(eval(input) == super_secret_string):
        if (something):
            print eval(input)[0] + ' is not a valid character\n'
            return
        print "nice, here's your flag" + flag
    else:
        print "You didn't guess the value of my super_secret_string\n"
```

Of course, most special functions were blocked so I couldn't view the flag directly.
With big credit to [http://wapiflapi.github.io/2013/04/22/plaidctf-pyjail-story-of-pythons-escape/](http://wapiflapi.github.io/2013/04/22/plaidctf-pyjail-story-of-pythons-escape/), we were able to create a string that would evaluate to another string, bypassing the input check. I stole the following from [https://ctftime.org/writeup/10677](https://ctftime.org/writeup/10677).

```python
def brainfuckize(nb):
    if nb in [-2, -1, 0, 1]:
        return ["~({}<[])", "~([]<[])",
                 "([]<[])",  "({}<[])"][nb+2]

    if nb % 2:
        return "~%s" % brainfuckize(~nb)
    else:
        return "(%s<<({}<[]))" % brainfuckize(nb/2)

def craftChar(n):
    beg = "`'%\xcb'`[{}<[]::~(~({}<[])<<({}<[]))]%("
    end = ")"
    mid = brainfuckize(n)

    return beg+mid+end

result = ""
for i in 'this_is_the_super_secret_string':
    result+= craftChar(ord(i))
    result+='+'

result = result[:-1]
```

# Restricted Shells

## No Letters

You can do tons of interesting things in a shell using shell expansions to call binaries even if you are restricted by the letters you can input. For example:

`/???/???/?????32` expands to /usr/bin/linux32, which will give you a simple dash shell. You could also run python using `/???/???/??????2`.
