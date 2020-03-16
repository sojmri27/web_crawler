#!/usr/bin/env python
# -*- coding: utf-8 -*-
from re import sub
import requests
from pymongo import MongoClient
from configparser import RawConfigParser

# ---------------- Get 591 Data --------------------------
def get_phone(id):
    req = requests.get(url = 'https://rent.591.com.tw/rent-detail-'+str(id)+'.html')
    text = req.text
    keywork = 'class="dialPhoneNum" data-value="'
    idx_s = text.find(keywork)+len(keywork)
    idx_e = text[idx_s:].find('">')
    return text[idx_s:idx_s+idx_e]
def covert_data(area, arr):
    data = []
    for d in arr:
        cond = d['condition']
        owner = d['linkman']
        owner_sex = ''
        if '小姐' in owner or '太太' in owner:
            owner_sex = 'girl'
        if '先生' in owner:
            owner_sex = 'boy'
        obj = {
            'area':area,
            'linkman':owner,
            'owner_sex':owner_sex,
            'role':d['nick_name'].split(' ')[0],
            'phone':get_phone(d['id']),
            'shape':d['shape'],
            'kind':d['kind'],
            'sex':'girl' if 'girl' in cond else 'boy' if 'boy' in cond else '',
            "updatetime": d['updatetime'],
            'info':d
        }
        data.append(obj)
    return data
def get_data(area, session, csrftoken):
    all_data = []
    try:
        url = 'https://rent.591.com.tw/home/search/rsList'
        jar = requests.cookies.RequestsCookieJar()
        jar.set('urlJumpIp', area)
        jar.set('591_new_session', session)
        headers = {'X-CSRF-TOKEN':csrftoken}
        total_cnt = 1
        cnt = 0
        while (len(all_data) < total_cnt) or (total_cnt==1 & cnt>=10):
            cnt+=1
            req = requests.get(url = url, params={'firstRow':len(all_data)}, headers=headers, cookies=jar)
            one_page_data = req.json()
            total_cnt = int(sub(r'[^\d.]', '', one_page_data['records']))  # 1,000 --> 1000
            all_data += covert_data(area, one_page_data['data']['data'])
        return all_data
    except Exception as e:
        print(str(e))
        return all_data

# ---------------- Insert Data ---------------------------
def parse_data(area, session, csrftoken, db, cfg):
    try:
        data = get_data(str(area), session, csrftoken)
        db[cfg["DB"]["table"]].insert_many(data)
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    cfg = RawConfigParser()
    cfg.read('config.ini')
    csrftoken = cfg["APIHeader"]["csrftoken"]
    session = cfg["APIHeader"]["session"]
    db = MongoClient('mongodb://'+cfg["DB"]["url"])[cfg["DB"]["name"]]
    # 台北市
    data_tpc = parse_data(1, session, csrftoken, db, cfg)
    # 新北市
    data_ntpc = parse_data(3, session, csrftoken, db, cfg)
    
    