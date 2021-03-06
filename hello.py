from flask import Flask, request
import urllib
from urllib2 import Request, urlopen, URLError
from datetime import datetime
import pdb
import simplejson as json

app = Flask(__name__)
ACCESS_TOKEN = 'f4106c6344a86aaa7805906ed9e2c411'
PERSONALITY_TOKEN = ''

@app.route('/agent_query', methods=['GET'])
def agent_query():
    params = request.args
    if 'mlsOfficeID' in params:
        mlsOfficeID = params.get('mlsOfficeID', '')

    url = 'https://rets.io/api/v1/armls/agents?access_token=%s&mlsOfficeID=%s&status=Active' %(ACCESS_TOKEN,20110829170205794604000000)
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

@app.route('/personal_query', methods=['GET'])
def personal_query():
    params = request.args
    if 'zipcode' in params:
        zipcode = params.get('zipcode', '')
    if 'downpayment' in params:
        downpayment = params.get('downpayment', '')


    data = personality(1)
    per = json.loads(data)
    opn = per.get('Openness', 0)
    con = per.get('Conscientiousness', 0)
    ext = per.get('Extraversion', 0)
    agr = per.get('Agreeableness', 0)
    neu = per.get('Neuroticism', 0)

    arr = []
    resultSingle = 0.2 * float(opn) + 0.3 * float(con) + 0.2 * float(ext) + 0.2 * float(agr) + 0.1 * float(neu)
    arr.append(resultSingle)
    resultCondominum = 0.1 * float(opn) + 0.2 * float(con) + 0.3 * float(ext) + 0.3 * float(agr) + 0.1 * float(neu)
    arr.append(resultCondominum)
    resultApartment = 0.4 * float(opn) + 0.1 * float(con) + 0.3 * float(ext) + 0.1 * float(agr) + 0.1 * float(neu)
    arr.append(resultApartment)
    resultTownhouse = 0.2 * float(opn) + 0.2 * float(con) + 0.3 * float(ext) + 0.1 * float(agr) + 0.2 * float(neu)
    arr.append(resultTownhouse)

    biggest = 0
    biggestIndex = 0
    for item in arr:
        if item > biggest:
            biggest = item
            biggestIndex = arr.index(item)
            #index of biggest number
    finalType = ""
    if biggestIndex == 0:
        finalType = "Single%20Family%20Residence"
    if biggestIndex == 1:
        finalType = "Condominium"
    if biggestIndex == 2:
        finalType = "Apartment"
    if biggestIndex == 3:
        finalType = "Townhouse"
    print finalType

    url = 'https://rets.io/api/v1/armls/listings?access_token=%s&status=Active&zipCode=%s&price[lt]=%s&subtype=%s' %(ACCESS_TOKEN,zipcode,int(downpayment)*5,finalType)
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
    body = ["156794164312", "700534096663194", "29438478619", "266960173414366", "6038767267", "90063435949", "117463815025618", "731359570308342", "944648888884263", "157750900979288", "1603548173244904", "1477865372436219", "130007087140416", "384381901588038", "741805665870458", "103820656323866", "1609680732580229", "1633781786861584", "274362492756946", "1069936086365702", "355374000182", "742909149057958", "283402178474385", "320726104664127", "796880707017716", "131033456938800", "404693309619224", "202825023077692", "538965869575549", "102099916530784", "139212906194976", "312906072120899", "1504566183150960", "177184462315697", "569505016493141", "70072372362", "314467614927", "239001756281046", "127559550648374", "110423472290", "125485372514", "154980601239560", "124730750929591", "776767052421359", "1590148551233065", "107918219228212", "291025411090034", "171112259610923", "183824211661952", "558570760836032", "100420534105", "356423544466920", "1471483279802294", "389699824542229", "160658967396083", "740963349331634", "52150999700", "844699408898230", "74133697733", "1564129283848675", "144333572255197", "268597136574561", "344153609078256", "598268693591136", "31732483895", "375146685900602", "1412406255640941", "1427235177572410", "1457718104460144", "275648462478015", "6815841748", "309473069184584", "57759776261", "302712573266439", "392695897476656", "435475646488178", "134474600022302", "1429281037340023", "267012543446119", "165872783507506", "144196652291747", "909177169096330", "443913262372306", "404217496261658", "154232664749642", "786779471358723", "122876494458807", "419286131560305", "1598144283750624", "322648407825917", "323607604501859", "195401730598414", "194000460667288", "1603454216543280", "1473230102918262", "773265706082055", "264199707117766", "109830840040", "1380970928814610", "120945717945722","759869860695450", "614700891971903", "131722800251844", "705307046230752", "299288473585838", "1398820670409048", "700153200065803", "80950130546", "183029809751", "626977713992838", "125068888682", "1460991510807357", "551387628231996", "1442649152647212", "103104823062518", "559334347500762", "411754008869486", "1458990554335457", "288745128002639", "1448428902098400", "91689589085", "392719867543072", "260878193996802", "193742123995472", "150793725009273", "259712900735014", "754165084605949", "229125047287911", "18807449704", "108358089365313", "22934684677", "6798562721", "178660838815620", "215431471814256", "524875554251304", "153674591314785", "528637977235766", "450043048401692", "105596369475033", "37627283118", "260431397453570", "630393896992288", "364244193645243", "423074604442367", "494270037370021", "188272077957844", "119702488081975", "250578768350947", "234057463385777", "1593224984237257", "145134942288090", "124037987606288", "1426267134282709", "226625490712161", "531808590208258", "172873029427580", "240741879315437", "129956967021642", "353982788022405", "472946459474440", "1424824314467982", "317928348241564", "596936260377653", "1513883428833863", "167633226631991", "509017515843172", "317694878281563", "207736459237008", "159746560708670", "244592802231250", "645971625453707", "606551219452245", "497325190397298", "1422421184702978", "77677035678", "275686972607176", "134880503350398", "398757826811605", "402935759809792", "274277002584642", "286631138179312", "1423830694520861", "537037206367456", "445704408813305", "723524834341607", "167708313289843", "244929708853349", "635463883209963", "413845295375731", "472025069592949", "280522108787910", "246544222164197", "307023978966", "606721589343692", "484635944970562", "624693740950745", "1571247986434375", "621639041196355", "135444303161125", "315523681851389","350672791615300", "515514761825666", "450818448336421", "148541531833925", "1422880871299863", "581908328556553", "415495551801558", "185455711646054", "12393266550", "210046452496565", "1426831737562846", "217176815111135", "316408078456157", "150627568320763", "296853740421530", "173110686205321", "144942248909694", "171693669620983", "118830248136274", "710642258980025", "256232277825653", "343997568977947", "635128009886167", "384381664992520", "362878653763901", "100913960079110", "649799061744255", "108755587572", "1452081275024219", "1543810285845169", "172789736206208", "114998944652", "5120148605", "171218912901660", "120349958044748", "504088899639641", "1410606279152927", "723341701031233", "223580667782938", "135609093117243", "442430012490396", "601169563263684", "573337389389619", "506826759390132", "180408965395760", "109380219087371", "31784218400", "85859466425", "191230157556928", "146123898794866", "1868209396651515", "514093821950781", "214961475221726", "701527203214409", "718084201543134", "111208545815", "174564976025110", "119888414741142", "332501813437268", "12138756141", "19366141168", "165442691420", "1436732216561261", "216311481960", "210305559023258", "100811203362272", "121866737894557", "166968980064117", "203595496347073", "23529603136", "163933470414859", "225299390951683", "125668460884134", "138659482947525", "247664788704910", "281867341834942", "759147870767231", "239036076177803", "106696649469001", "174697985977319", "268504409849240", "410852228944681", "232540186777278", "578114692269502", "276620012351729", "169552423070535", "78986534109", "454568751294577", "78082761961", "183613205058056", "187553811409640", "522186261196752", "1398540293721088", "144456422792", "182764008595803", "451836741536694", "180048600476", "521817007851858", "62309496693", "121866094648108", "115545381802707", "617657864964594", "122837181099458", "475160835856379", "622711894416595", "111090485635468", "16804585819", "166389413387501", "148284605181868", "312625645503340", "26435256798", "201672210934", "109878972400482", "56381779049", "247962661966966", "144549515641267", "182846775060765", "188800678017", "153464388031637", "609293025782647", "114732793365", "104550952956141", "332498280134792", "491327050920567", "213179268798946", "88792296524", "241806149201604", "139908942723217", "325389540940675", "194158510604782", "19297198192", "586487838060776", "29286157460", "107777555911981", "357597640985163", "682842015075690", "25498833315", "478232665560749", "212107522223904", "228628480523843", "9329881766", "287142134710", "60839262877", "100484820802", "68471055646", "145864485469478", "176309402425319", "128239567371216", "474905629264197", "488356901209621", "229145477207495", "134007550044757", "349971245085513", "164147683642700", "170901143077174", "454634434599119", "238531559492836", "141819636003404", "276205255801477", "418837278196322", "69448024527", "304028842982306", "56470170364", "369958449790624", "367116489976035", "106378526110722", "233224836695428", "7227076742", "127460964060503", "137350106366177", "237164486349270", "328362360617522", "226018137415109", "208048135883430", "476054662412666", "184289921605682", "92304305160", "248019911970829", "100340306738294", "443489549003913", "129476993842648", "82627199176", "114721225206500", "226162457410985", "65217182024", "112158795467813", "177993572219306", "104072652962475", "214123981941462", "334556859937345", "112335462112397", "11215611028", "131161116925915", "194839529381", "132989670121245", "133481940001233", "135455263166569", "110729172284893", "109594812392024", "113242012023271",]

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


@app.route('/user_beacon', methods=['GET'])
def user_beacon():
    f = open('user_beacon.json', 'r')
    data = json.loads(f.read())

    return json.dumps(data )


@app.route('/beacon_in', methods=['POST'])
def beacon_in():

    params = request.args
    uid = int(params.get('uid', ''))
    bid = int(params.get('bid', ''))

    f = open('user_beacon.json', 'r')
    data = f.read()
    f.close()
    if data:
        USER_BEACON = json.loads(data)
    else:
        USER_BEACON = {}

    params = request.args
    uid = params.get('uid', '')
    bid = params.get('bid', '')


    if uid not in USER_BEACON:
        data = USER_BEACON[uid] = {}  #  {bid1: {'in':time_in, 'out':time_out},
                                      #   bid2: {'in':time_in, 'out':time_out} }
    else:
        data = USER_BEACON[uid]

    data[bid] = {}
    data[bid]['in'] = datetime.utcnow().strftime('%c')


    print "Successfully saved!"


    f = open('user_beacon.json', 'w')
    json.dump(USER_BEACON, f)
    f.close()

    print json.dumps(USER_BEACON)
    flask.redirect(flask.url_for('user_beacon'))


@app.route('/beacon_out', methods=['POST'])
def beacon_out():
    f = open('user_beacon.json', 'r')
    data = f.read()
    f.close()
    if data:
        USER_BEACON = json.loads(data)
    else:
        USER_BEACON = {}

    params = request.args
    uid = params.get('uid', '')
    bid = params.get('bid', '')

    if uid not in USER_BEACON:
        return
    else:
        data = USER_BEACON[uid]

    if bid not in data:
        return
    else:
        data[bid]['out'] = datetime.utcnow().strftime('%c')
        in_time = datetime.strptime(data[bid]['in'], '%c')
        out_time = datetime.strptime(data[bid]['out'], '%c')
        beacon_total = out_time - in_time
        data[bid]['total'] = beacon_total.total_seconds()

    user_total = 0
    for k in data.keys():
        if type(data[k]) == dict and 'total' in data[k]:
            user_total += data[k]['total']
    if user_total > 0:
        data['total'] = user_total

    print "Successfully saved!"
    f = open('user_beacon.json', 'w')
    json.dump(USER_BEACON, f)
    f.close()
    print json.dumps(USER_BEACON)
    flask.redirect(flask.url_for('user_beacon'))


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



# curl -v -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{bid1: {'in':time_in, 'out':time_out},bid2: {'in':time_in, 'out':time_out} } '  http://localhost:5000//beacon_out/
