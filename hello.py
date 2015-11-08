from flask import Flask, request
import urllib
from urllib2 import Request, urlopen, URLError
import pdb
import json

app = Flask(__name__)
ACCESS_TOKEN = 'f4106c6344a86aaa7805906ed9e2c411'
PERSONALITY_TOKEN = ''
USERS = {}


@app.route('/personal_query', methods=['GET'])
def personal_query():
    params = request.args
    if 'zipcode' in params:
        zipcode = params.get('zipcode', '')
    if 'downpayment' in params:
        downpayment = params.get('zipcode', '')
    
    data = personality(1)    
    per = json.loads(data)
    o = per.get('Openness', 0)
    e = per.get('Extraversion', 0)
    con = per.get('Conscientiousness', 0)

    url = 'https://rets.io/api/v1/armls/listings?access_token=%s&status=Active&zipCode=%s&price[lt]=%s&acres[lt]=%s' % (ACCESS_TOKEN, zipcode, downpayment*5, o*10)
    
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


@app.route('/personality/<user_id>', methods=['GET'])
def personality(user_id):
    token = get_auth_token()
    url = 'http://api-v2.applymagicsauce.com/like_ids?uid=1057067830970640'

    req = Request(url)
    header = {'X-Auth-Token': token,'Content-Type': 'application/json','Accept': 'application/json'}
    for k,v in header.items():
        req.add_header(k,v)
    body = ['626977713992838','147528418608788','7568536355','219078791517770','1418357048442480','1494537294109740',
     '29601460857','108692325878093','7312612866','127801184032925','14693100218','261406207269503','196985620414852','679911962047519',
     '686877424698830','187459867951418','7218745779','683151028429631','427120970660412','188361071196107','17295379437','12161711085',
     '107748965915008','584508934992916','149515305173840','62309496693','661804540571055','303198611518','1512306032325880',
     '293751410757388','17043549797','35546482165','1579064862319634','143754018709','82777273087','164937920216067',
     '105625442803392','6452638289','131722800251844']

    try:
        response = urlopen(req, json.dumps(body))
    except URLError, e:
        print 'Check api_key/customer_id. Got an error code:', e

    if response.getcode() == 200:
        big5 = dict()
        data = json.loads(response.read()).get('predictions', [])
        if data:
            for row in data:
                if row.get('trait', '') == 'BIG5_Openness':
                    big5['Openness'] = row.get('value')
                if row.get('trait', '') == 'BIG5_Conscientiousness':
                    big5['Conscientiousness'] = row.get('value')
                if row.get('trait', '') == 'BIG5_Extraversion':
                    big5['Extraversion'] = row.get('value')
                if row.get('trait', '') == 'BIG5_Neuroticism':
                    big5['Neuroticism'] = row.get('value')
                if row.get('trait', '') == 'BIG5_Agreeableness':
                    big5['Agreeableness'] = row.get('value')
                    
        return json.dumps(big5)
    return 'Response object empty'


def get_auth_token():
    url = 'http://api-v2.applymagicsauce.com/auth'
    auth = Request(url)
    auth.add_header('Content-Type', 'application/json')
    data = {
        'customer_id': '1999',
        'api_key': 'jtf5djsvl7kdmkttl5efar5hh6'
    }
    try:
        response = urlopen(auth, json.dumps(data))
    except URLError, e:
        print 'Check api_key/customer_id. Got an error code:', e        
    if response.getcode() == 200:
        data = json.loads(response.read())      
        token = data.get('token', '')
        PERSONALITY_TOKEN = token           
        return token
    return 
    

# @app.route('/beacon_in', methods=['POST'])
# def in_beacon(user_id, time):
#     params = request.args
#     if 'user_id' in params:
#         uid = params.get('user_id', '')
#     if 'time' in params:
#         time = params.get('time', '')
    
#     data = USERS[user_id] = []
#     data[len(data)]['in'] = time 

# def out_beacon(user_id):
    

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

    url = 'https://rets.io/api/v1/armls/listings?access_token=%s&status=Active&zipCode=%s&price[lt]=%s' % \
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
