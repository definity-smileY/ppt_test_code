import requests as rq
import json
import os
import sys
import urllib.request
import collections
import pymongo
from pymongo import MongoClient
import requests 

url = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json"
res = rq.get(url, params={"address":'서울특별시' + ' ' + '마포구'}) 
jdata = res.json()

e = jdata['stores']
addr = []
name = []
remain = []


for idx in range(0, len(e)):
    addr.append(e[idx]['addr'])
    name.append(e[idx]['name'])
    remain.append(e[idx]['remain_stat'])
    
    print(e[idx]['remain_stat'])



