import base64
import json
import urllib

import requests

import time
import hmac
import hashlib

API_URL = "https://api.naver.com"


def getNow() -> int:
    now = time.time()
    return now


def getSignature(path: str, method: str, API_SECRET: str) -> tuple:
    time = int(getNow())
    message = '{}.{}.{}'.format(time, method, path)
    signature = base64.b64encode(hmac.new(API_SECRET.encode(), msg=message.encode(),
                                          digestmod=hashlib.sha256).digest())
    return signature, time


def getCampagins(API_KEY: str, API_SECRET: str, CUSTOMER_ID: str) -> list:
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


def getAdsGroups(API_KEY: str, API_SECRET: str, NCC_CAMPAIGN_Id: str, CUSTOMER_ID: str) -> list:
    PATH = "/ncc/adgroups"
    QUERY = {
        'nccCampaignId': NCC_CAMPAIGN_Id
    }

    ses = requests.Session()
    signature, time = getSignature(PATH, "GET", API_SECRET)
    res = ses.get(API_URL + PATH, headers={
        "X-API-KEY": API_KEY,
        "X-Signature": signature,
        "X-Timestamp": str(time),
        "X-CUSTOMER": CUSTOMER_ID,
    }, params=QUERY)
    return res.json()


def getAdsGroups(API_KEY: str, API_SECRET: str, CUSTOMER_ID: str) -> list:
    pass


def setIpExclusion(API_KEY: str, API_SECRET: str, CUSTOMER_ID: str, ip: str) -> list:
    PATH = "/tool/ip-exclusions"
    body = {
        "filterIp": ip
    }

    ses = requests.Session()
    signature, time = getSignature(PATH, "POST", API_SECRET)
    res = ses.post(API_URL + PATH, headers={
        "X-API-KEY": API_KEY,
        "X-Signature": signature,
        "X-Timestamp": str(time),
        "X-CUSTOMER": CUSTOMER_ID,
        'Content-Type': 'application/json'
    }, data=json.dumps(body))
    return res.json()


def deleteIpExclusion(API_KEY: str, API_SECRET: str, CUSTOMER_ID: str, ids: list) -> list:
    PATH = "/tool/ip-exclusions"

    ses = requests.Session()
    signature, time = getSignature(PATH, "DELETE", API_SECRET)
    res = ses.delete(API_URL + PATH, headers={
        "X-API-KEY": API_KEY,
        "X-Signature": signature,
        "X-Timestamp": str(time),
        "X-CUSTOMER": CUSTOMER_ID,
        'Content-Type': 'application/json'
    }, params={"ids": ids})
    return res.status_code
