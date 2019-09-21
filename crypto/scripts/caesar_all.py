import sys

text = sys.argv[1]
text = text.lower()
shifts = []

for i in range(1, 27):
	word = ""
	for j in range(0, len(text)):
		if text[j:j+1].isalpha() == True:
			newASCII = ord(text[j:j+1]) + i
			if newASCII >= 122:
				newASCII = 96 + newASCII - 122
			word = word + chr(newASCII)
		else:
			word = word + text[j:j+1]
	shifts.append(word)

for i in range(len(shifts)):
	print("{:02}".format(i) + ": " + shifts[i])
