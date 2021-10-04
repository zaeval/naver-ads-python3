import base64
import requests

import time
import hmac
import hashlib

API_URL = "https://api.naver.com"


def getNow() -> int:
    now = time.time()
    return now

def getSignature(path:str, method:str, API_SECRET:str) -> tuple:
    time = int(getNow())
    message = '{}.{}.{}'.format(time, method, path)
    signature = base64.b64encode(hmac.new(API_SECRET.encode(), msg=message.encode(),
                                          digestmod=hashlib.sha256).digest())
    return signature, time

def getCampagins(API_KEY:str, API_SECRET:str, CUSTOMER_ID:str) -> list:
    PATH = "/ncc/campaigns"

    ses = requests.Session()
    signature, time = getSignature(PATH, "GET", API_SECRET)
    res = ses.get(API_URL + PATH, headers={
        "X-API-KEY": API_KEY,
        "X-Signature": signature,
        "X-Timestamp": str(time),
        "X-CUSTOMER": CUSTOMER_ID,
    })
    return res.json()

def tests():
    customer_id = ""
    API_SECRET = ''
    api_key = ''

    campaigns = getCampagins(api_key,API_SECRET,customer_id)

    campaignId = campaigns[0]["nccCampaignId"]
    print(campaignId)


tests()
