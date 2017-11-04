from pwn import *
import pprint as pp
import time

##########################
### ECB Decrypt Script ###
##########################

# Constants
server = "crypto.chal.csaw.io"
port = 1578
blocksize = 16

# Guess how long the message you're trying to read is.
# If you'd like the program to guess, leave as -1
message_length = -1

# Guess the desired message size
if message_length == -1:
	r = remote(server, port)
	r.sendlineafter(": ", "")
	response = r.recvline()
	message_length = len(response.split()[3]) / 2
	r.close()
	print("Guessing message length of {} bytes".format(message_length))

# Initialization
first_chunk  = bytearray("A" * message_length)
second_chunk = bytearray("A" * (message_length - 1))
decrypted_bytes = bytearray()
start_time = time.time()
for byte_num in range(message_length):

	# Percent completed
	now_time = time.time()
	print("[{}]: {}% complete - {}".format(time.strftime('%H:%M:%S', time.gmtime(int(now_time - start_time))), round(byte_num * 1.0 / message_length * 100, 1), decrypted_bytes))

	# Brute force last byte of second chunk
	second_chunk = bytearray("A" * (message_length - byte_num - 1))

	# Create the first chunk whose encrypted value gets checked against the second chunk's encrypted value
	num_leading_As = len(second_chunk)
	num_decrypted = len(decrypted_bytes)
	remaining_As = message_length - num_leading_As - num_decrypted
	first_chunk = bytearray("A" * num_leading_As) + decrypted_bytes + bytearray("A" * remaining_As)

	# Begin brute force
	r = remote(server, port)
	decrypted_byte = -1
	for i in range(256):

		if not chr(i).isspace(): # CSAW problem said no spaces
			first_chunk[message_length - 1] = i
			payload = first_chunk + second_chunk
			payload = ''.join([chr(x) for x in payload])

			# Receive prompt
			r.recvuntil(": ")
			r.sendline(payload)
			response = r.recvline()
			response_blocks = response.split()[3]

			# Split response into blocks of blocksize * 2 characters. This is because each hex char is half a byte.
			response_blocks = [response_blocks[x:x+blocksize * 2] for x in range(0, len(response_blocks), blocksize * 2)]

			# Group into first and second
			first_cipher_chunk = ''.join([response_blocks[x] for x in range(message_length / blocksize)])
			second_cipher_chunk = ''.join([response_blocks[x] for x in range(message_length / blocksize, message_length / blocksize * 2)])

			# Check if we guessed the byte right
			if first_cipher_chunk == second_cipher_chunk:
				decrypted_byte = i
				decrypted_bytes = decrypted_bytes + bytearray(chr(decrypted_byte))
				break

	# Move on to next byte
	r.close()

	if decrypted_byte == -1:
		print("Failed to decrypt! Must be some logic bug")
		exit(1)

print("[{}]: {}% complete".format(time.strftime('%H:%M:%S', time.gmtime(int(now_time - start_time))), 100.0))
print(decrypted_bytes)
