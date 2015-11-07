from flask import Flask, request
from urllib2 import Request, urlopen, URLError
import pdb
import json

app = Flask(__name__)
ACCESS_TOKEN = 'f4106c6344a86aaa7805906ed9e2c411'

@app.route('/query', methods=['GET'])
def query():	
	
	params = request.args
	
	if 'zipcode' in params:
		zipcode = params.get('zipcode', '')
	if 'price' in params:
		price = params.get('price', '')
	
	if not price:
		price = 1000
	if not zipcode:
		zipcode = 94102

	url = 'https://rets.io/api/v1/test/listings?access_token=%s&zipCode=%s&price[lt]=%s' % \
		(ACCESS_TOKEN, zipcode, price)
	
	print zipcode
	print price

	query = Request(url)
	try:
		response = urlopen(query)
		data = response.read()

		if type(data) == str:
			body = json.loads(data)
			if body.get('status', '') == 200:
				listings = body.get('bundle', {})
				return json.dumps(listings)
		return 'no data'
	except URLError, e:
	    print 'No kittez. Got an error code:', e
    	

if __name__ == '__main__':
    app.run()
