---
title: forensics
date: 2018-05-04 18:17:08
---

# Git
When you have a .git folder and want to see a history of all the commits:
```
git log --patch
```

View specific commit hashes:
```
git show
```

# Disk Images
If you want to carve out files from a disk image, try using foremost.
Note that foremost will print out the binaries to the console which may crash it - make sure to redirect output somewhere.
```
foremost image -o
```
