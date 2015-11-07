from flask import Flask, request
import urllib
from urllib2 import Request, urlopen, URLError
import pdb
import json

app = Flask(__name__)
ACCESS_TOKEN = 'f4106c6344a86aaa7805906ed9e2c411'

@app.route('/personality', methods=['GET'])
def personality():
    token = get_auth_token()
    url = 'http://api-v2.applymagicsauce.com/like_ids'
    req = Request(url)
    header = {
        'X-Auth-Token': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    body = {
        'traits': 'BIG5_Openess',
        'uid': '1063389267005163'
    }
    for k,v in header.items():
        req.add_header(k,v)
    req.add_data(urllib.urlencode(body))
    
    try:
        response = urlopen(req)        
    except URLError, e:
        print 'Check api_key/customer_id. Got an error code:', e
    
    if response.getcode() != 200:
        data = json.loads(response.read())
        token = data.get('token', '')
        return token
    return 'token'

def get_auth_token():
    url = 'http://api-v2.applymagicsauce.com/auth'
    auth = Request(url)
    auth.add_header('Content-Type', 'application/json')
    data = {
        'customer_id': '1997',
        'api_key': 'vhhllbncv79i3gcr0m7p89pit3'
    }
    try:
        response = urlopen(auth, json.dumps(data))
        if response.getcode() == 200:
            data = json.loads(response.read())      
            token = data.get('token', '')
            PERSONALITY_TOKEN = token           
            return token
        return 
    except URLError, e:
        print 'Check api_key/customer_id. Got an error code:', e


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

    url = 'https://rets.io/api/v1/armls/listings?access_token=%s&zipCode=%s&price[lt]=%s' % \
        (ACCESS_TOKEN, zipcode, price)    
    query = Request(url)
    try:
        response = urlopen(query)        
    except URLError, e:
        print 'No kittez. Got an error code:', e
    
    data = response.read()
    if type(data) == str:
        body = json.loads(data)
        if body.get('status', '') == 200:
            listings = body.get('bundle', {})
            return json.dumps(listings)
    return 'no data'

if __name__ == '__main__':
    app.run()
