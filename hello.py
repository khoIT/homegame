from flask import Flask, request
from urllib2 import Request, urlopen, URLError
import pdb
import json

app = Flask(__name__)
ACCESS_TOKEN = 'f4106c6344a86aaa7805906ed9e2c411'

@app.route('/', methods=['GET'])
def hello():
	return 'HomeGame server'

@app.route('/query', methods=['GET'])
def query():
	params = request.args
	if 'zipcode' in params:
		zipcode = params.get('zipcode', '')
	else:
		zipcode = 94103
	if 'price' in params:
		price = params.get('price', '')
	else:
		price = 1000000

	url = 'https://rets.io/api/v1/test_sf/listings?access_token=%s&zipCode=%s&price[lt]=%s' % \
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
