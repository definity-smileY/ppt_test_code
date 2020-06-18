import requests as rq
import json
import os
import sys
import urllib.request
import collections
import pymongo
from pymongo import MongoClient



def dofiles():
    # 몽고디비 연결 클라이언트
    # 1.몽고디비 클라이언트 연결객체 생성
    client = MongoClient('mongodb://localhost:27017/')
    # -- 객체생성확인
    print('client.HOST: {0}'.format(client.HOST))

    # 2. 데이터베이스 생성
    ydb = client['hyu_py']
    # -- 디비 생성 확인
    print(ydb)

    # 3. 컬렉션 객체 생성
    
    keys = ydb.keys
    ydb.keys.remove()
    def ykkk(addr):
        url = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json"

        # 응답코드(status_code) 반환
        # 200: 성공, 404: 존재하지 않는 url
        res = rq.get(url, params={"address":addr}) #rq.post()
        #print(res.status_code)
        if res.status_code == 200:
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
        
        return jdata

    def insertMongo(pWords):
        
        
        keys_cs = [ {'store': pWords} ]

        #5. 여러개의 데이터 입력
        rst_keys = keys.insert_many(keys_cs)
        print(rst_keys)
    
    def some():
        for key in keys.find():
            print(key)



    
    menus = ['나가기', '지역입력/데이터베이스저장', '데이터베이스불러오기']
    sel_index = 0
    print("== TEST START! ==")
    while True:
        # 메뉴출력
        print('== MENU LIST ==')
        for m in range(0, len(menus)):
            print('%d.%s' % (m, menus[m]))

        sel_index = input('CHOICE : ')

        # 선택별 진행
        if sel_index == '0':
            print("== THE END ==")
            break
        elif sel_index == '1': # 인경우            
            vKey = input('지역 , 구 :'  )
            words = ykkk(vKey)
            insertMongo(words)
        elif sel_index == '2':
            some()
        

# 프로그램 실행
dofiles()

print("=== THE END ===")




