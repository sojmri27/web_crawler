#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from pymongo import MongoClient
from configparser import ConfigParser
from bson.json_util import dumps
import re

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
cfg = ConfigParser()
cfg.read('config.ini')
db = MongoClient('mongodb://'+cfg["DB"]["url"])[cfg["DB"]["name"]]

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        args = request.args
        query = {}
        for key in ['sex', 'area', 'phone', 'isowner', 'linkman', 'owner_sex']:
            val = args.get(key, '')
            if len(val)==0:
                continue
            if key in ['phone', 'linkman']:
                query[key] = re.compile(val)
                continue
            if key == 'sex':
                query[key] = { "$in": [val, ""] }
                continue
            if key == 'isowner':
                if val == 'true':
                    query['role'] = '屋主'
                else:
                    query['role'] = {'$ne':'屋主'}
                continue
            query[key] = val
        data = db[cfg["DB"]["table"]].find(query, {'_id': 0, 'area': 1, 'linkman': 1,'role':1, 'phone':1, 'shape':1, 'sex':1, 'info.fulladdress':1, 'info.room':1, "info.area"
: 1, 'info.price' : 1, 'info.condition':1, 'info.kind_name':1, 'info.floor':1})
        return dumps(data)
    except Exception as e:
        print(str(e))
        return '<span style="color:red;font-weight:bold;">System Error</span>'
if __name__ == '__main__':
    app.debug = True
    app.run()