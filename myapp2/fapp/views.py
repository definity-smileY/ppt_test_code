import numpy as np
import re
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django import forms
from django.views.generic import CreateView
from django.http import JsonResponse
import json
from fapp.apimongo import doFiles, insertUserid, doJusoApi, insertAddrs, selCollection, selDocument, doNavApiXml, doNavApi2, makeTestDeviationdb 
from fapp.worldcup.world_cup import world ######
from fapp.apimask_t import ydofiles
from collections import Counter
from fapp.tClass import tClassName #from 폴더이름.파이썬이름 import 클래스이름
import folium

from fapp.tClass import tClassName
from fapp.tClassOtP import tClassOtParent
from fapp.tClassChildMP import tClassChildCMParent as cmp 

from fapp.ChildMP_I import ClassChildCMParent_I as cmpi

from fapp.form_.LoginFrm import LoginFrm
from django.forms import BaseForm

from fapp.form_.jusoFrm import jusoF as jf
import urllib.request
from django.shortcuts import redirect

import csv
from django.http import HttpResponse

from fapp.form_.meanFrm import Meanfrm as mf
from fapp.form_.deviationFrm import Devifrm as df

import math, numpy


def world_view(request):
    return render(request,"fapp/world_view.html",{"title":"월드컵정보","content":world()})


# ========================= 편차폼 출력
def go_deviation(request):
    df_= df
    return render(request, "fapp/go_deviation.html", { "title": "표준편차실습", "message": "표준편차", "mf_": df_})  

# ========================= 편차 컬렉션 생성/저장
def go_deviation_save(request):
    print('request.GET.get("id_theme"):' + request.GET.get("id_theme"))
    id_theme = request.GET.get("id_theme")
    # 몽고디비에 테스트 데이터 생성
    json_list = makeTestDeviationdb(id_theme)
    # 평균 print(json_list[0]['monenies'][0]['money'])
    # json집합
    jsons = { 'items' : []}
    # json각자
    jsoni = {}
    
    meanv = 0 # 평균
    deviationv = 0
    deviationvs = []
    json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    print("=============================================")
    for i in json_list:
        means = []   # 평균데이터
        # 급여평균
        print(i["name"])
        for m in i["monenies"]:
            means.append(m['money'])
        # 평균 means.append(i["monenies"])
        meanv = np.round(numpy.mean(means))
        print('평균 : ' + str(meanv))
        # 표준편차
        deviationv = np.round(np.std(means))
        deviationvs.append(deviationv)
        print('표준편차 : ' + str(deviationv))

        jsoni = { 'name' :  i["name"], 'meanv' : meanv, 'deviationv' : deviationv }
        jsons['items'].append(jsoni)
    
    # 급여가 제일 안정적인 사람
    print('# 급여가 제일 안정적인 사람')
    deviationvmin = np.min(deviationvs)
    #print(deviationvmin)
    deviationvminman = {}

    # 급여가 제일 불안정적인 사람
    print('# 급여가 제일 불안정적인 사람')
    deviationvmax = np.max(deviationvs)
    #print(deviationvmin)
    deviationvmaxman = {}

    for itm in jsons['items']:
        # 급여가 제일 안정적인 사람
        if itm['deviationv'] == deviationvmin:
            deviationvminman = itm
        # 급여가 제일 불안정적인 사람
        if itm['deviationv'] == deviationvmax:
            deviationvmaxman = itm
        
    print(deviationvminman['name'])
    print(deviationvmaxman['name'])
    # for m in jsons['items']['deviationv']:
        # print(str(m['deviationv']))

    allcon = []
    # 사람들
    allcon.append(jsons['items'])
    # 급여가 제일 안정적인 사람
    allcon.append(deviationvminman)
    # 급여가 제일 불안정적인 사람
    allcon.append(deviationvmaxman)
    

    # 편차
    return JsonResponse(allcon,content_type='application/json', safe=False,json_dumps_params={'ensure_ascii':False})





# 요청시 실행될 메서드들
# 가.서치후 몽고DB에 저장
# 1. 요청시 방가! 장고 텍스트를 리턴
def rtnBangga(request):
    return HttpResponse("방가? 윤우섭!")

def doMessage(request):
    #문장출력
    return render(
        request, "fapp/message.html", {"title": "메세지타이틀","message":"메세지","content":"메세지 컨텐트입니다."}
    )
# 2. 문장출력
def doMessage2(request):
    # 검색어 / 컬렉션이름을 받아서 검색하고 몽고디비에 저장
    #json_list = doNavApiXml(request.GET.get('selClass'),request.GET.get('txtColname'))
    json_list = doFiles(request.GET.get('selClass'),request.GET.get('txtColname'))
    json_list = Counter(json_list)
    return JsonResponse(json_list.most_common(10),content_type='application/json', safe=False,json_dumps_params={'ensure_ascii':False})

def doDate(request):
    #문장출력
    return render(
        request,"fapp/date.html", {"title":"데이트타이틀","date":datetime.now(tz=None),"content":"데이트 컨텐트입니다."}
    )    

def doTime(request):
    #문장출력
    return render(
        request,"fapp/time.html", {"title":"데이트타이틀","date":datetime.now(tz=None),"content":"타임 컨텐트입니다."}
    )


def doMask2(request):
    # 검색어 / 컬렉션이름을 받아서 검색하고 몽고디비에 저장
    json_list = ydofiles(request.GET.get('yselClass'),request.GET.get('ytxtColname'))

    return JsonResponse(json_list,content_type='application/json', safe=False,json_dumps_params={'ensure_ascii':False})

def doMask(request):
    #문장출력
    return render(
        request, "fapp/mask.html"

    )

#============= 그래프시작
def message_graph_pie2(request):
    # 검색어 / 컬렉션이름을 받아서 검색하고 몽고디비에 저장
    #json_list = doNavApiXml(request.GET.get('selClass'),request.GET.get('txtColname'))
    json_list = doFiles(request.GET.get('selClass'),request.GET.get('txtColname'))
    json_list = Counter(json_list)
    
    jsonlistmc = json_list.most_common(10)
    return JsonResponse(jsonlistmc,content_type='application/json', safe=False,json_dumps_params={'ensure_ascii':False})

def message_graph_pie(request):
    return render(request, 'fapp/message_graph_pie.html', {"title": "그래프", "message": "그래프 ㅋㅋ", "content": "그래프 컨텐트입니다. "
    })
#=============그래프종료
def domap(request):
    #문장출력
    return render(request, "fapp/map.html",{"map": "맵"})

#================차트테스트
def graph_pie2(request):
    json_list = ydofiles(request.GET.get('yselClass'),request.GET.get('ytxtColname'))
    return JsonResponse(json_list,content_type='application/json', safe=False,json_dumps_params={'ensure_ascii':False})

def graph_pie(request):
    return render(request,'fapp/graph_pie.html') 

def chart_pie(request):
    return render(request, "fapp/chart.html")

# 4.AJAX요청 doNavApi
def page_move1_proc(request):
    # 검색어 / 컬렉션이름을 받아서 검색하고 몽고디비에 저장
    #json_list = doNavApiXml(request.GET.get('selClass'),request.GET.get('txtColname'))
    json_list = doFiles(request.GET.get('selClass'),request.GET.get('txtColname'))
    json_list = Counter(json_list)
    return JsonResponse(json_list.most_common(50),content_type='application/json', safe=False,json_dumps_params={'ensure_ascii':False})

# 폼화면
def page_move1(request):
    return render(request, "fapp/page_move1.html", { "title": "페이징타이틀", "message": "페이징 ㅋㅋ", "content": "페이징 컨텐트입니다. "})


# 요청시 실행될 메서드들
def page_class(request):
    resValue = tClassName.testParent()

    return render(request, "fapp/page_class.html",{"title":"클래스 스터디 타이틀","message":"클래스 스터디 페이징ㅋㅋ",
"content1":"(8+9)="+str(resValue),"content2":"tClassName.vPrarent = "+str(tClassName.vPrarent)})


# 다중상속 요청시 실행될 메서드들
def page_class_mp(request):
    # cmp.vChildMParent:자식의어트리뷰트
    # cmp.vPrarent:첫번째 자식의 
    # cmp.vPrarentOt 
    vFamily = cmp.vChildMParent + cmp.vPrarent + cmp.vPrarentOt

    return render(request, "fapp/page_class_mp.html",{"vFamily":"부모클래스 2개와 자식클래스 1 개의 변수의 합(vFamily)= " + str(vFamily), "testChildMParent":"자식의 함수리턴 값 (testChildMParent()) = " + str(cmp.testChildMParent()),"testParent":"첫번째 부모의 함수리턴 값(testParent()) = " + str(cmp.testParent()),"testOtParent":"두번째 부모의 함수리턴 값(testOtParent()) = " + str(cmp.testOtParent())})

# 인터페이스 요청시 실행될 메서드들
def page_inserface_mp(request):
    tvFamily = cmpi.testOtParent() + "," + cmpi.testParentI() + "," + cmpi.testChildMParentI()

    return render(request, "fapp/page_inserface_mp.html",{"tvFamily":"부모인터페이스2개와 자식클래스 1개의 메서드 리턴 값 =" + tvFamily})

# 로그인 폼
def go_login(request):
    lf = LoginFrm()

    return render(request,"fapp/go_login.html",{"lf":lf})

# 로그인 폼 : 아이디 등록
def go_login_proc(request):
    # 검색어/ 컬렉션이름을 받아서 검색하고 몽고디비에 저장
    # json_list = doNavApiXml(request.GET.get('selClass'),request.GET.get('txtColname'))
    id_userid = request.GET.get("id_userid")
    print(id_userid)
    insertUserid(id_userid)

    return JsonResponse(id_userid,content_type='application/json',safe=False,json_dumps_params={'ensure_ascii' : False})
# 가입 폼
def go_juso(request):
    jf_ = jf()
    print('여기!')
    # 포스트방식
    if request.method == 'POST':
        print('저기!')
        jf_ = jf(request.POST)
        print(jf_.is_valid())
        print(jf_)
        # if request.method == 'POST': 데이터를 제대로 받았는지 확인
        if jf_.is_valid():
            # jf_.cleaned_data 클래스로 가져온 데이터를 json으로 정리
            cd = jf_.cleaned_data
            print(cd)
            insertAddrs(cd)
        return redirect('/fapp/go_juso/', kwargs={ "title": "가입폼 클래스 스터디 타이틀", "message": "가입폼 스터디 페이징 ㅋㅋ", "jf_": jf_})

    return render(request, "fapp/go_juso.html", { "title": "가입폼 클래스 스터디 타이틀", "message": "가입폼 스터디 페이징 ㅋㅋ", "jf_": jf_})

    
def go_juso_proc(request):
    # 검색어 / 컬렉션이름을 받아서 검색하고 몽고디비에 저장
    # json_list = doNavApiXml(request.GET.get('))
    addrs = doJusoApi(request, pKey = request.GET.get("pKey"))
    print(addrs)
    return JsonResponse(addrs,content_type='application/json', safe=False,json_dumps_params={'ensure_ascii':False})


# 머신러닝
# ========================= 평균폼 출력
def go_gmean(request):
    mf_= mf

    return render(request, "fapp/go_gmean.html", { "title": "평균실습", "message": "빈도수가 상위 10인 데이터중에서 10개의 빈도수 평균보다 높은 데이터만 차트로 출력", "mf_": mf_})  

# ========================= 평균 컬렉션 수집/저장
def go_gmean_save(request):
    print('request.GET.get("id_theme"):' + request.GET.get("id_theme"))
    doFiles(pKey = request.GET.get("id_theme"), pColname=request.GET.get("id_theme"))
    print(selCollection())
    return JsonResponse(selCollection(),content_type='application/json', safe=False,json_dumps_params={'ensure_ascii':False})
     
# ========================= 평균 처리
def go_gmean_proc(request):
    # 검색어 / 컬렉션이름을 받아서 검색하고 몽고디비에 저장
    #json_list = doNavApiXml(request.GET.get('selClass'),request.GET.get('txtColname'))
    # print('request.GET.get("id_theme_sel") : ' + request.GET.get('id_theme_sel'))
    json_list = doFiles(request.GET.get('id_theme_sel'), request.GET.get('id_theme_sel'))
    json_list = Counter(json_list)
    # 10개
    top10 = json_list.most_common(10)
    print('=============')
    print(top10[0][1])
   # 합계
    sume = 0
    # 평균
    means = []
    

    for t in top10:
        sume = sume + t[1]
        means.append(t[1])

    # 평균구하기
    meanv = numpy.mean(means)

    # 전송할 배열
    allcon = []
    allcon.append(top10)
    allcon.append(meanv)
    allcon.append(sume)
    
    # 평균
    return JsonResponse(allcon,content_type='application/json', safe=False,json_dumps_params={'ensure_ascii':False})
