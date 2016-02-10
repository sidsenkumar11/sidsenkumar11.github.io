import hashlib
import sys

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


with open("cars.txt", "r") as file:
	cars = file.read().split('\n')

with open("numbers.txt", "r") as file:
	numbers = file.read().split('\n')

with open("punctuation.txt", "r") as file:
	punctuation = file.read().split('\n')

hash = "f82fae9becc67392b1bdf9a9ba753d8c7838f0aa0e806455625875bdf0992122"

for i in range(0, len(cars)):
	permutations = []
	recurse("", cars[i], permutations)
	print(cars[i])
	for carPerm in permutations:
		for j in range(0, len(numbers)):
			for k in range(0, len(numbers)):
				for l in range(0, len(numbers)):
					for m in range(0, len(punctuation)):
						word = carPerm + numbers[j] + numbers[k] + numbers[l] + punctuation[m]
						n = hashlib.sha256(word).hexdigest()
						if n == hash:
							print(word)
							sys.exit("found")