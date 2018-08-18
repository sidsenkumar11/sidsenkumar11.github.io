---
title: radare
date: 2018-05-05 16:25:27
---

### Starting R2
r2 crackme0x06
aa # Analyze All
aaa # Analyze all Functions

### Graph View
`VV @ main` - Enter graph view for main function
`hjkl` - Scroll
`HJKL` - Scroll Faster
`.` - Center the block on the screen
`p` - Cycle through graph view types
`tab` - Go to next node
`t/f` - Follow true/false edges
`u` - undo movement - equivalent of Esc in IDA
`x <number>` - x brings up functions form which the current function is called. 0 is to choose which one to go to.

### Rename Variables
`afvn original_name new_name`
`r` - Refresh graph

### Rename Functions
`afn original_function_name new_function_name`
`r` - Refresh graph
`d`  - Rename a function in graphical mode.
`dr` - Rename a function otherwise.

### Comments
`CCu "Comment text" @0x8048...` - Adds comment above this line
(alternatively: `CCa 0x8040... "Comment Text"`)
`CC- @0x8048...`  - Deletes comment at this line. Can't delete comment given by r2
Don't put semicolons in comments if you want them to appear at another line using `CCu`.

### Go Into Call / Function
`g[function_letter]` - Next to the call, there is a command (eg. [gc]). Typing gc would take you into the function
# If you are in visual mode and not graph mode, just enter the number in comments in the shell.

### View Shell Inside Graph View
`:` - Just press the colon

### Strings
`iz` - Find all strings
`iz ~ flag.txt` - Take output of iz and grep for "flag.txt"
`/ flag.txt` - Search for the string flag.txt

### Find Xrefs
`axt <address>` - xrefs to strings
`axt sym.imp.printf` - xrefs to functions

### Seek
`s <address or function_name>` - Seek to address or function name
`us` - Undo Seek

### View disassembly
`pdf @ main` - Print disassembly function
`pdf` - Print disassembly from current location
`pd <number>` - Print first number lines of disassembly

### Commands
`x`  - Go back via xrefs.
`_`  - Search for symbols

TODO
===========
View all symbols / functions
Format the comments so they appear neater (eg. vertically aligned)
Edit an existing comment that r2 generated for me
Remove an existing comment that r2 generated for me
Highlight all occurrences of variable or function call
How to go back a function after going to another one in visual mode (equivalent of ESC in IDA)
Rename jump target (basic block beginning)
