def calc_key(cipher, plain, IV):
	# Input is hex string arrays
	# Ex. cipher = ["42", "8a", "ff", "16"]
	# key = plain ^ cipher ^ IV
	key = []
	for i in range(len(cipher)):
		key.append(int(cipher[i], 16) ^ int(plain[i], 16) ^ int(IV[i], 16))
	return key

# Decrypt a single block in CBC
def xor_block(cipherblock, key, old_cipherblock):
	# Input is integer array with each integer being the byte value
	# Ex: cipherblock = [249, 23, 161, 200]
	result_block = []
	for i in range(len(cipherblock)):
		result_block.append(cipherblock[i] ^ key[i] ^ old_cipherblock[i])
	return result_block

# Decrypt all cipher blocks and write to a file
def decrypt(ciphertext, key, IV, extension, blocksize=4):

	# CBC Decryption
	decrypted = []
	old_cipher = IV

	for x in range(0, len(ciphertext) - blocksize, blocksize):
		plain_block = xor_block(ciphertext[x:x+blocksize], key, old_cipher)
		decrypted.extend(plain_block)
		old_cipher = ciphertext[x:x+blocksize]

	# Write result to file
	decrypted = bytearray(decrypted)
	with open("decrypted." + extension, "wb") as f:
		f.write(decrypted)

if __name__ == "__main__":

	# Given
	filename = "bricks_of_gold_40d12e05cd6d67ed51d29a6da39d6878"
	IV = "43 41 53 48".split()
	cipher_header = "24 58 4D 54".split()

	# Guess different file headers
	# JPG, PNG, GIF, PDF
	poss_extens = ["jpg", "gif", "png", "pdf"]
	poss_plains = ["FF D8 FF E0", "47 49 46 38", "89 50 4e 47", "25 50 44 46"]
	for i in range(len(poss_plains)):
		poss_plains[i] = poss_plains[i].split()

	# Save possible keys
	poss_keys = []
	for plain in poss_plains:
		poss_keys.append(calc_key(cipher_header, plain, IV))

	# Open encrypted file data into integer byte array
	ciphertext = []
	with open(filename, "rb") as f:
		byte = f.read(1)
		ciphertext.append(int.from_bytes(byte, byteorder='little'))
		while byte:
			# Do stuff with byte.
			byte = f.read(1)
			ciphertext.append(int.from_bytes(byte, byteorder='little'))


	# Convert IV into integer array
	IV = [int(x, 16) for x in IV]

	# Decrypt file by each extension
	for i in range(len(poss_keys)):
		decrypt(ciphertext, poss_keys[i], IV, poss_extens[i])

	print("Done!")
