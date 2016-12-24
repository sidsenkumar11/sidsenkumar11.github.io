import base64

# The name of the file to read in and output file
fileName = "obj3_dump.txt"
outFileName = "hex.txt"

# Read the file in, get rid of any new line characters
with open(fileName, "r") as myfile:
	data = myfile.read().replace('\n', '')

# Decode the string as base 64
data = base64.b64decode(data)

# Convert the base64 string to hex
data = data.encode("hex")

# Write the data to an output file
with open(outFileName, 'w') as f:
	f.write(data)
