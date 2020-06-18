import json
import os
import sys
import urllib.request
import collections
import pymongo
from pymongo import MongoClient
from xml.dom import minidom
from xml.etree import ElementTree
from collections import Counter
from bson.json_util import dumps
import datetime, random

def makeTestDeviationdb(pColname):

    # 몽고디비 연결 클라이언트
    # 1.몽고디비 클라이언트 연결객체 생성
    client = MongoClient('mongodb://localhost:27017/')
    # -- 객체생성확인
    print('client.HOST: {0}'.format(client.HOST))

    # 2. 데이터베이스 생성
    mdb = client['devidb']
    # -- 디비 생성 확인
    print(mdb)

    # 3. 컬렉션 객체 생성
    mdb[pColname].remove()
    coln = mdb[pColname]

    # 이름/급여일/금액 : 3명, 3개월
    myDevis = []
    monenies = []
    for i in range(1,11):
        # 1월6월까지 급여 지급액
        for j in range(1,7):
            monenies.append({'date': datetime.datetime(2020, j, 20), 'money': random.randrange(100,1000)})
        jone = { "name" : "이름"+str(i), 'monenies':monenies}
        myDevis.append(jone)
        monenies = []

    #5. 여러개의 데이터 입력
    coln.insert_one({'myDevis':myDevis})
    #print(rst_keys)
    return myDevis



# 디비의 컬렉션의 도큐먼트 가져오기
def selDocument(theme_sel):
    # 몽고디비 연결 클라이언트
    # 1.몽고디비 클라이언트 연결객체 생성
    client = MongoClient('mongodb://localhost:27017/')
    # -- 객체생성확인
    print('client.HOST: {0}'.format(client.HOST))

    # 2. 데이터베이스 생성
    mdb = client['mdb_py']
    # -- 디비 생성 확인
    docs = dumps(mdb[theme_sel].find())
    print(docs)
    return docs

# 디비의 컬렉션 목록 가져오기
def selCollection():
    # 몽고디비 연결 클라이언트
    # 1.몽고디비 클라이언트 연결객체 생성
    client = MongoClient('mongodb://localhost:27017/')
    # -- 객체생성확인
    print('client.HOST: {0}'.format(client.HOST))

    # 2. 데이터베이스 생성
    mdb = client['mdb_py']
    # -- 디비 생성 확인
    print(mdb.list_collection_names())
    return mdb.list_collection_names()


def doNavApi2(pKey, pColname):
    words = []
    
    # 스트링을 받아 특정기호를 제거해 주는 함수
    def remove_any(pTarget, pChars):
        for c in pChars:
            pTarget = pTarget.replace(c, '')
        return pTarget

    # 네이버에서 가져온 데이터를 단어로 분리해 배열로 리턴
    def getNavNews(pKey):
        client_id = "uGdNY2mjnpUZNU_XDzU4"
        client_secret = "2xVDF0pbRH"

        # 파라미터
        encText = "&".join(["query="+urllib.parse.quote(pKey)
        , "display=100"
        , "start=1"
        ])
        url = "https://openapi.naver.com/v1/search/news?" + encText

        # json 결과
        # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if(rescode==200):
            response_body = response.read()
            #print(response_body.decode('utf-8'))
            # json
            u8_json = response_body.decode('utf-8')
            # 파이썬 json 객체
            j = json.loads(u8_json)

            # 반복문으로 출력

            word = []
            for it in j["items"]:
                word = remove_any(it["title"], ['\n','&quot;','.',',',',',"'","‘","’","[","]","→","/","&gt","…","·",'“','”','&lt;',';','!','?','</b>','<b>','(',')','⑫','...'])
                words.extend(word.split(' '))
            #print(words)
            json_list = Counter(words)
            json_list = json_list.most_common(10)
            for wd in json_list:
                print(wd)
            return words
        else:
            print("Error Code:" + rescode)

    def insertMongo(pWords):

        # 몽고디비 연결 클라이언트
        # 1.몽고디비 클라이언트 연결객체 생성
        client = MongoClient('mongodb://localhost:27017/')
        # -- 객체생성확인
        print('client.HOST: {0}'.format(client.HOST))

        # 2. 데이터베이스 생성
        mdb = client['djangodb']
        # -- 디비 생성 확인
        print(mdb)

        # 3. 컬렉션 객체 생성
        mdb[pColname].remove()
        keys = mdb[pColname]

        keys_cs = [ {'words': pWords} ]

        #5. 여러개의 데이터 입력
        keys.insert_many(keys_cs)
        #print(rst_keys)

    # 스크래핑후 몽고db저장
    words = getNavNews(pKey)
    insertMongo(words)

    return words


    
# 주소정보 몽고디비에 저장
def insertAddrs(pJson):
    # 몽고디비 연결 클라이언트
    # 1.몽고디비 클라이언트 연결객체 생성
    client = MongoClient('mongodb://localhost:27017/')
    # -- 객체생성확인
    print('client.HOST: {0}'.format(client.HOST))

    # 2. 데이터베이스 생성
    mdb = client['djangodb']
    # -- 디비 생성 확인
    print(mdb)

    # 3. 컬렉션 객체 생성
    # mdb[pColname].remove()
    keys = mdb['addrs']

    #5. 여러개의 데이터 입력
    keys.insert_one(pJson)

# 도로명 API결과 JSON으로 받기
# http://www.juso.go.kr/addrlink/jusoSearchSolutionIntroduce.do
def doJusoApi(request, pKey):
    # 초기
    pKey = urllib.parse.quote(pKey)
    url = "http://www.juso.go.kr/addrlink/addrLinkApi.do?currentPage=1&countPerPage=10&keyword="+pKey+"&confmKey=devU01TX0FVVEgyMDIwMDUyMDE2MDg0ODEwOTc3ODk=&resultType=json"

    # 주소 json 결과 받기 : 
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        # 주소 json 결과 처리 : 
        response_body = response.read()
        # 파이썬 json 객체
        u8_json = response_body.decode('utf-8')
        j = json.loads(u8_json)
        print(type(j))

        roadAddr = []
        #print(j)
        for it in j["results"]["juso"]:
            roadAddr.append(it['roadAddr'])
        print(roadAddr)
    else:
        print("Error Code:" + rescode)
    return roadAddr


def doFiles(pKey, pColname):
    words = []
    # 스트링을 받아 특정기호를 제거해 주는 함수
    def remove_any(pTarget, pChars):
        for c in pChars:
                pTarget = pTarget.replace(c, '')
        return pTarget

    # 네이버에서 가져온 데이터를 단어로 분리해 배열로 리턴
    def getNavNews(pKey):
        client_id = "uGdNY2mjnpUZNU_XDzU4"
        client_secret = "2xVDF0pbRH"

        # 파라미터
        encText = "&".join(["query="+urllib.parse.quote(pKey)
        , "display=100"
        , "start=1"
        ])
        url = "https://openapi.naver.com/v1/search/news?" + encText

        # json 결과
        # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if(rescode==200):
            response_body = response.read()
            #print(response_body.decode('utf-8'))
            # json
            u8_json = response_body.decode('utf-8')
            # 파이썬 json 객체
            j = json.loads(u8_json)

            # 반복문으로 출력
            word = []
            for it in j["items"]:
                word = remove_any(it["title"], ['\n','&quot;','.',',',',',"'","‘","’","[","]","→","/","&gt","…","·",'“','”','&lt;',';','!','?','</b>','<b>','(',')','⑫','...'])
                words.extend(word.split(' '))
            print(words)
            return words
        else:
            print("Error Code:" + rescode)

    def insertMongo(pWords):

        # 몽고디비 연결 클라이언트
        # 1.몽고디비 클라이언트 연결객체 생성
        client = MongoClient('mongodb://localhost:27017/')
        # -- 객체생성확인
        print('client.HOST: {0}'.format(client.HOST))

        # 2. 데이터베이스 생성
        mdb = client['mdb_py']
        # -- 디비 생성 확인
        print(mdb)

        # 3. 컬렉션 객체 생성
        mdb[pColname].remove()
        keys = mdb[pColname]
        keys_cs = [ {'words': pWords} ]

        #5. 여러개의 데이터 입력
        rst_keys = keys.insert_many(keys_cs)
        print(rst_keys)
      

    # 스크래핑후 몽고db저장
    words = getNavNews(pKey)
    insertMongo(words)

    return words
        
def doNavApiXml(pKey, pColname):
    words = []
    # 스트링을 받아 특정기호를 제거해 주는 함수
    def remove_any(pTarget, pChars):
        for c in pChars:
                pTarget = pTarget.replace(c, '')
        return pTarget

    # 네이버에서 가져온 데이터를 단어로 분리해 배열로 리턴
    def getNavNews(pKey):
        client_id = "uGdNY2mjnpUZNU_XDzU4"
        client_secret = "2xVDF0pbRH"
        encText = urllib.parse.quote("검색할 단어")
        url = "https://openapi.naver.com/v1/search/news.xml?query=" + encText # json 결과
        # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            #print(response_body.decode('utf-8'))
            root = ElementTree.fromstring(response_body)
            #xmldoc = ElementTree.dump(root)
            #print(root.tag)
            #for child in root:
            #    print(child.tag, child.attrib)
            #print(root[0][0])
            #print(root[0][0].text)
            #print(root[0].findall("item"))
            #print(root[0].find("title").text)
            #print(root[0].find("item")[0].text)
            #print(type(root.findall("item")))
            lists = root[0].findall("item")
            word = []
            for obj in lists:
                print(obj.find("title").text)
                word = remove_any(obj.find("title").text, ['\n','&quot;','.',',',',',"'","‘","’","[","]","→","/","&gt","…","·",'“','”','&lt;',';','!','?','</b>','<b>','(',')','⑫','...'])
                words.extend(word.split(' '))
            print(words)
            return words
        else:
            print("Error Code:" + rescode)
            # 반복문으로 출력

    def insertMongo(pWords):

        # 몽고디비 연결 클라이언트
        # 1.몽고디비 클라이언트 연결객체 생성
        client = MongoClient('mongodb://localhost:27017/')
        # -- 객체생성확인
        print('client.HOST: {0}'.format(client.HOST))

        # 2. 데이터베이스 생성
        mdb = client['mdb_py']
        # -- 디비 생성 확인
        print(mdb)

        # 3. 컬렉션 객체 생성
        mdb[pColname].remove()
        keys = mdb[pColname]

        keys_cs = [ {'words': pWords} ]

        #5. 여러개의 데이터 입력
        rst_keys = keys.insert_many(keys_cs)
        print(rst_keys)

    # 스크래핑후 몽고db저장
    words = getNavNews(pKey)
    insertMongo(words)

    return words

# 프로그램 실행
# doNavApi("정치", "testcol")

# print(" == ALL END == ")

# 프로그램 실행
# doFiles("정치", "testcol")

# print(" == ALL END == ")

# 아이디 등록
def insertUserid(pUserid):
    # 몽고db 연결 클라이언트
    # 1.몽고db 클라이언트 연결객체 생성
    client = MongoClient('mongodb://localhost:27017/')
    # 객체 생성 확인
    print('client.HOST:{0}'.format(client.HOST))

    # 2. 데이터베이스 연결
    mdb = client['djangodb']
    # db생성 확인
    print(mdb)

    # 3. 컬렉션 객체 생성
    keys = mdb['useridc']
    # _id : 오라클의 프라이머리키
    _id = {'_id': pUserid}

    # 4. 여러개의 데이터 입력
    keys.insert_one(_id)