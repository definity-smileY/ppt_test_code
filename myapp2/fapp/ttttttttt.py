import requests as rq
import json
import os
import sys
import urllib.request
import collections
import pymongo
from pymongo import MongoClient
import requests 

def ydofiles(ykey, ycolname):
    yywords = []
    
    def getmask(ykey, ycolname):
        url = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json"

        
        # 응답코드(status_code) 반환
        # 200: 성공, 404: 존재하지 않는 url
        res = rq.get(url, params={"address":ykey + ' ' + ycolname}) #rq.post()
        
        #print(res.status_code)
        if res.status_code == 10:
            print("[요청성공]")
        else:
            print("[알수 없는 에러:%s]\n" % res)

        # load json data
        jdata = res.json()
        
        #print(type(jdata)) # 데이터 타입 확인용(dict)
        #print(jdata) # 데이터 확인용

        #2 주요 데이터표시

        cnt = 0
        for store in jdata['stores']:
            # remain_stat : none, empty, few, some, plenty
            # empty : 회색(0~1개)/few:빨강색(2~29개)/
            # some: 노랑색(30~99개)/ plenty: 녹색 (100개이상)
            status = store.get('remain_stat')
            if status in ["few","some","plenty"]:
                cnt+=1
                print(store['name'], ":",status)
                print(store['addr'])
                print("입고일: ", store.get('stock_at'))
                print("생성일: ", store.get("created_at"))
                print("{:-^30}".format(cnt))

        print(cnt)
        
        return jdata


        
        
    def insertMongo(yWords):

        # 몽고디비 연결 클라이언트
        # 1. 몽고디비 클라이언트 연결객체 생성
        client = MongoClient('mongodb://localhost:27017/')
        # 객체 생성확인
        print('client.HOST: {0}'.format(client.HOST))

        # 2. 데이터베이스 생성
        ydb = client['mask_py']
        # 디비 생성 확인
        print(ydb)

        # 3. 컬렉션 객체 생성
        ydb[ycolname].remove()
        ykeys = ydb[ycolname]

        ykeys_cs = [ {'address' : yWords} ]

        # 4. 여러개의 데이터 입력/여러개 컬렉션 입력
        yrst_keys = ykeys.insert_many(ykeys_cs)
        print(yrst_keys)
    
    # 스크래핑후 몽고db저장
    yywords = getmask(ykey, ycolname)
    insertMongo(yywords)

    return yywords

    ##컬렉션을 찾아보자
print(ydofiles('서울특별시','마포구'))

#프로그램 실행
# dofiles("서울특별시","마포구")
# print(" == ALL END == ")
