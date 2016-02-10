import string
import itertools

key = 3
keys = {} # Dict to store values
for each in string.printable: # All possible values that could have been encrypted
    if not str(ord(each) // key) in keys.keys():
        keys[str(ord(each) // key)] = [each]
    else:
        keys[str(ord(each) // key)].append(each)
#make keys
message = "27 39 33 34 10 36 32 33 35 10 37 34 10 38 35 34 37 38 15 15 15 10 33 32 38 40 33 38 34 41 34 36 16 16 38 31 33 16 39 35 38 35 16 36 41"
message = message.split()
dec = [keys[x] for x in message]

#print a table
lineOne = ""
lineTwo = ""
lineThree = ""
for each in dec:
	lineOne = lineOne + each[0] + " | "
	if (len(each) > 1):
		lineTwo = lineTwo + each[1] + " | "
		lineThree = lineThree + each[2] + " | "
	else:
		lineTwo = lineTwo + " " + " | "
		lineThree = lineThree + " " + " | "
	#print(each)
print(lineOne)
print(lineTwo)
print(lineThree)