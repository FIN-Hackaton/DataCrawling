
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
import requests
import json
import logging
import pymongo
import time
import os

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
    'Referer': 'https://m.land.naver.com/'
}

URL = "https://m.land.naver.com/cluster/ajax/articleList?itemId=&mapKey=&lgeo=&showR0=&rletTpCd=APT&tradTpCd=A1%3AB1%3AB2&z=12"

f = open("gu1.txt", "r")
# mongodb 서버에 연결하는 로직
load_dotenv(verbose=True)
MONGO_URI = os.getenv('MONGO_URI')
connection = pymongo.MongoClient(MONGO_URI)
db = connection['real']
db.naver.drop()
naver = db.naver

for i in f:
    try:
        data = {}
        #print(type([i]))
        #for j in range(7):
        data2 = i.strip('{').strip('}\n').split(',')
        #print(data2[0].split(":"))
        for k in range(len(data2)):
            d = data2[k].strip("'").split(":")
            data[d[0].strip().strip("'")] = d[1].strip().strip("'")
        lat = data['lat']
        lon = data['lon']
        cortarNo = data['cortarNo']
        cortarNm = data['cortarNm']

    except IndexError:
        pass

    param = {
        'lat': lat,
        'lon': lon,
        'cortarNo':cortarNo,
        'sort':'rank',
    }
    
    logging.basicConfig(level=logging.INFO)
    page = 0

    while True:
        page += 1
        param['page'] = page

        resp = requests.get(URL, params=param, headers=header)
        if resp.status_code != 200:
            logging.error('invalid status: %d' % resp.status_code)
            break

        data = json.loads(resp.text)
        result = data['body']
        if result == []:
            logging.error('no result')
            break
        
        for item in result:
            naver.insert_one({"atclNm":item['atclNm'],"rlettpCd":item['rletTpCd'],"tradTpNm" : item['tradTpNm'], "bildNm" : item['bildNm'], "flrInfo" : item['flrInfo'], "prc":item['prc'], 'cpNm' : item["cpNm"], "cortarNo":item["cortarNo"]})
            #logging.info('[%s] %s %s층 %s만원 %s %s' % (item['tradTpNm'], item['bildNm'], item['flrInfo'], item['prc'], item['cpNm'], item['cortarNo']))
        time.sleep(10)
        print(page)
        