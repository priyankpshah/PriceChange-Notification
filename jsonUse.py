import json
import requests
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient
from Token import ACCSID,AUTH_TOKEN



class PriceChangeNot:
    def __init__(self,url):
        self.URL = url

    def loadUrl(self):
        hdr = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(self.URL)
        return r

    def dataExtract(self,r):
        soup = BeautifulSoup(r.content, "lxml")
        letters = soup.find_all(id="productSEOData")
        reldata = letters[0].get_text()
        return reldata

    def JsonLoad(self,reldata):
        jsonData = json.dumps(json.loads(reldata), sort_keys=True, indent=4, separators=(',', ': '))
        jsonData = json.loads(jsonData)
        if 'price' in jsonData['offers']:
            myprice = jsonData['offers']['price']
        else:
            myprice = jsonData['offers'][0]['price']
        return myprice,jsonData['name']

    def priceMatch(self,price,name):
        pass

    def UserNotification(self,price,name):
        client = TwilioRestClient(ACCSID,AUTH_TOKEN)
        client.messages.create(to_="+13126473207", from_="+18722405791", body=price + name)


URL = "https://www.macys.com/shop/product/calvin-klein-mens-minneapolis-overcoat?ID=2891313&CategoryID=3763&tdp=cm_app~zMCOM-NAVAPP~xcm_zone~zPDP_ZONE_A~xcm_choiceId~zcidM05RRM-a1f11e94-4fff-4cce-9ac2-7de75506cda1%40H7%40customers%2Balso%2Bshopped%243763%242891313~xcm_pos~zPos3"
pc = PriceChangeNot(URL)
r = pc.loadUrl()
data = pc.dataExtract(r)
price,name = pc.JsonLoad(data)

name = "Product Name: "+name
price = "Current Price: $"+price+"  "

pc.UserNotification(price,name)




