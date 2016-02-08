def recurse (pref,suff, words):
    # If no characters left, just print prefix.

    if suff == "":
            words.append(pref)
            return

    # Otherwise add lowercase of first suffix letter to prefix
    # and recur with that and the remainder of the suffix.
    # Then do the same for uppercase.
    # If you wanted smarts, this is where you'd detect if the
    # upper and lower were the same and only recurse once.

    recurse (pref + suff[0:1].lower(), suff[1:], words)
    recurse (pref + suff[0:1].upper(), suff[1:], words)


# HOW TO USE:
permutations = []
recurse("", "Ben", permutations)
print(permutations)