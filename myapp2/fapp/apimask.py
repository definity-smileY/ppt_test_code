import requests
import json
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import numpy as np

#def getmaskstore(): 마스크를 판매하는 판매처의 정보가 담긴 함수(재고정보x)
#def getmaskstat(): 마스크의 재고상황이 담긴 함수 (판매처청보x)
#def getcode(판매처정보,재고정보): 판매처 정보와 재고정보를 code값을 통해 하나로 합쳐주는 함수

# 데이터들을 csv형태로 만들어주기
def getMaskStore():
    #total_page 를 가져오기 위해
    url = 'https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/sales/json?page=1'
    req = requests.get(url)
    total_page = req.json()['totalPages']

    #약국정보에 대해서 가져올 부분
    addr = [] #주소
    code = [] #식별코드
    latitude = [] #위도
    longitude = [] #경도
    name = [] #이름
    types = [] # 판매처 유형

    for i in range(1,total_page+1): #totalpage 가 54이기 때문에 +1을 해줘야한다.
        url = 'https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/stores/json?page='+str(i) # 각 페이지들 불러오기
        req = requests.get(url)
        storeInfo = req.json()['storeInfos'] #json 안의 store정보 가져오기
        for j in storeInfo: #아까 만든거 안에 append 해준다
            addr.append(j['addr'])
            code.append(j['code'])
            latitude.append(j['lat'])
            longitude.append(j['lng'])
            name.append(j['name'])
            types.append(j['type'])

    #넣어준걸로 데이터 프레임 만들어주기
    df_maskStoreInfo=pd.DataFrame({'addr':addr,"code":code,'lat':latitude,'name':name,'tpye':types})
    
    #return
    return df_maskStoreInfo

mask_store_info = getMaskStore()
#print(mask_store_info)

def getMaskStat():
    url = 'https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/sales/json?page=1'
    req = requests.get(url)
    total_page = req.json()['totalPages']

    stat={} # 딕셔너리 생성
    for i in range(1,total_page+1):
        url = 'https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/sales/json?page='+str(i)
        req = requests.get(url)
        sales = req.json()['sales']
        for j in sales:
            try:
                stock_at = j['stock_at']
            except:
                stock_at = 'none'
            if stock_at != 'Invalid date':
                code=j['code']
                created_at=j['created_at']
                try:
                    remain_stat=j['remain_stat']
                except:
                    remain_stat='none'

                stat[code] = {'created_at':created_at,'remain_stat':remain_stat,'stock_at':stock_at}    

    return stat

mask_stat_info = getMaskStat()

drop_mask_store_info = mask_store_info.dropna(axis=0) #공백을 없애주는

def getCode(drop_mask_store_info,mask_stat_info):
    #stat과 store 코드의 개수가 다른거 기억하기
    code = drop_mask_store_info['code']
    
    created_at = []
    remain_stat = []
    stock_at = []
    
    for i in range(len(code)):
        try: #코드가 있는 경우
            created_at.append(mask_stat_info[code[i]]['created_at'])
            remain_stat.append(mask_stat_info[code[i]]['remain_stat'])
            stock_at.append(mask_stat_info[code[i]]['stock_at'])
        except: #코드가 없는 경우
            created_at.append('none')
            remain_stat.append('none')
            stock_at.append('none')

    #이제 합쳐줘야함 (데이터[칼럼명]=들어갈거)
    drop_mask_store_info['created_at']=created_at
    drop_mask_store_info['remain_stat']=remain_stat
    drop_mask_store_info['stock_at']=stock_at
    
    return drop_mask_store_info

get_mask_info = getCode(drop_mask_store_info,mask_stat_info)
#get_mask_info.to_csv('mask_info.csv',index=False)

#데이터셋을 지도에 표현
#folium 잘 작동되나 해보기
seoul = [37.541,126.986]
m = folium.Map(location=seoul, tiles="OpenStreetMap",zoom_start=10)

#이름 , 위도,경도를 가져와주기
get_store_lnfo = get_mask_info.loc[:,['name','lat','lag','created_at','remain_stat','stock_at']]

#.loc[:,['','']] 이름으로 열 가져오기
name=list(get_store_lnfo['name'])
lat =list(get_store_lnfo['lat'])
lng =list(get_store_lnfo['lng'])
remain_stat = list(get_store_lnfo['remain_stat'])
stock_at = list(get_store_lnfo['stock_at'])
colorList ={'plenty':'green','some':'orange','few':'red','empty':'gray','break':'black','none':'blue'}
amount={'plenty':'100개이상','some':'30개이상 100개 미만','few':'2개이상 30개미만','empty':'다팔려버렸다','break':'판매중지','none':'정보없음'}
#지도에 표시해주기 위해 MarkerCluster 을 사용해준다.
#location=[위도경도],popup=이름 , icon
Marker_Cluster = MarkerCluster().add_to(m)
for i in range(len(name)):

    folium.Marker(
    location = [lat[i],lng[i]],
    popup= '약국이름 : '+name[i]+'\n입고시간 : '+stock_at[i]+'\n재고상태 : '+amount[remain_stat[i]],
    icon=folium.Icon(color=colorList[remain_stat[i]],icon='ok')
    ).add_to(MarkerCluster)

m.save('map.html') #html 파일로 저장