import pandas as pd
import csv
import json
import os
import sys
import urllib.request
import collections
import pymongo
from pymongo import MongoClient
from xml.dom import minidom
from xml.etree import ElementTree

def world():

    df = pd.read_csv('D:/projs/FIFA 2018 Statistics.csv',error_bad_lines=False,index_col=False)

    #print(df.head())
    #dfhead = str(df.head())
    #print(type(dfhead))

    #df.head() 불러온 csv파일 요약해서 보기
    # print(df) : csv확인하기
    # print(type(df)) : csv 자료형 확인하기
    # print(df.columns) : csv 항목 구별하기
    # print(df.columns[1]) : 각 항목에 숫자를 통해 개별적 접근 확인하기
    # print(df.index)# : 인덱스 확인하기
    # print(df[:3]) : 처음 세줄 확인하기
    # print(df.head(4)) : head를 써서 처음 data 읽기
    # print(df.tail()) : 마지막 date 읽기
    # print(df['Goal Scored'].sum()) : 그 항목의 원소들만 불러오기
    # print(df['Goal Scored'].mean()) : 그 항목의 평균을 불러오기
    # print(df['Goal Scored'].std()) : 그 항목의 표준편차 불러오기
    # print(df.set_index('Team')) : 팀으로 바꾸기
    # print(df.set_index('Team').loc['Korea Republic'])
    # print(df.set_index('Team').loc['Korea Republic'].mean()) : 한국팀의 표준편차 불러오기

    team_list = df.set_index('Team').index # 국가별 정리하기
    team = [] # 중복되는 나라이름 빼기
    for i in team_list:
        if i not in team:
            team.append(i)

    #print(team)
    team_summary = {} # data에 대한 접근key를 나라이름으로 하기
    for i in range(len(team)):
        team_summary[team[i]] = df.set_index('Team').loc[team[i]].mean()
    
    # print(team_summary['Korea Republic'])
    # print(team_summary['Korea Republic'][13]) # 나라들 중 가장 파울을 많이 범한 나라
    # data = []
    fouls = {}
    goals = {}
    possession = {}
    distance = {}
    yellow_and_red = {}
    pass_accuracy = {}
    teamsum={}
    for i in range(len(team)):
        fouls[team[i]] = team_summary[team[i]][13]
        goals[team[i]] = team_summary[team[i]][0]
        possession[team[i]] = team_summary[team[i]][1]
        pass_accuracy[team[i]] = team_summary[team[i]][9]
        distance[team[i]] = team_summary[team[i]][11]
        yellow_and_red[team[i]] = team_summary[team[i]][15]
        teamsum[team[i]] = [team_summary[team[i]][13], team_summary[team[i]][0]]
        

    
    #print(team_summary['Korea Republic'])
    # print(max(fouls, key=fouls.get))
    # data = [fouls, goals, possession, distance, yellow_and_red, pass_accuracy]
    # print(data)
    #print ('가장 골 많이 넣은 나라 : {}'.format(max(goals, key=goals.get)))
    goals = max(goals, key=goals.get)
    # print(goals)
    # print ('가장 점유율 높은 나라 : {}'.format(max(possession, key=possession.get)))
    #print ('가장 패스 정확도 높은 나라 : {}'.format(max(pass_accuracy, key=pass_accuracy.get)))
    #print ('가장 뛴거리가 많은 나라 : {}'.format(max(distance, key=distance.get)))
    #print ('가장 경고 & 퇴장 많이 받은 나라 : {}'.format(max(yellow_and_red, key=yellow_and_red.get)))

    score = {} # 가장 아름다운 축구를 한 나라를 불러오기
    for i in range(len(team)):
        score[team[i]] = team_summary[team[i]][0]*2 + team_summary[team[i]][1]*0.1 + team_summary[team[i]][9]*0.15 + team_summary[team[i]][11]*0.005 - team_summary[team[i]][15]
        #print(score[team[i]])
    #print('가장 아름다운 축구를 한 나라 : {}'.format(max(score, key=score.get)))
    #print('가장 더럽게 축구를 한 나라 : {}'.format(min(score, key=score.get)))
    score = max(score, key=score.get),min(score, key=score.get)
    data = score,goals,teamsum
    return data

def insertUserid(pUserid):
    # 몽고db 연결 클라이언트
    # 1.몽고db 클라이언트 연결객체 생성
    client = MongoClient('mongodb://localhost:27017/')
    # 객체 생성 확인
    print('client.HOST:{0}'.format(client.HOST))

    # 2. 데이터베이스 연결
    mdb = client['world']
    # db생성 확인
    #print(mdb)
    mdb['all'].remove()

    # 3. 컬렉션 객체 생성
    keys = mdb['all']
    
    # _id : 오라클의 프라이머리키

    keys_cs = [ {'words': pUserid} ]

    #5. 여러개의 데이터 입력
    keys.insert_many(keys_cs)

insertUserid(world())