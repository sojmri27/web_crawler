#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def csv_to_df(typ):
    df = pd.read_csv("plvr_land_data/"+typ+"_lvr_land_a.csv", skiprows=[1])
    return df
def read_csv():
    df_a = csv_to_df('a')
    df_b = csv_to_df('b')
    df_e = csv_to_df('e')
    df_f = csv_to_df('f')
    df_h = csv_to_df('h')
    df = pd.concat([df_a, df_b, df_e, df_f, df_h], ignore_index=True)
    return df

def check_floor_1(str):
    if str is None or str is np.nan:
        return False
    arr_floor = ['一層', '二層', '三層', '四層', '五層', '六層', '七層', '八層', '九層', '十層', '十一層', '十二層']
    return str not in arr_floor
def check_floor_2(str):
    if str is None or str is np.nan:
        return False
    floor = 0
    numbers = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
    }
    last = ''
    for v in str.replace("層", ""):
        if v == '十' and len(last) > 0:
            last_num = numbers.get(last, 0)
            floor -= last_num
            floor += last_num*10
            continue
        last = v
        floor += numbers.get(v, 0)
    return floor >= 13
def export_a(df):
    is_home = df['主要用途']=='住家用'
    is_building = df['建物型態'].str.contains('住宅大樓') # df['建物型態'] == '住宅大樓(11層含以上有電梯)'
    is_floor = df['總樓層數'].apply(check_floor_2) # df['總樓層數'].apply(check_floor_1)
    filter_a = df[is_home & is_building & is_floor]
    filter_a.to_csv('filter_a.csv', index = False, header=True)
def export_b(df):
    filter_b = pd.DataFrame({'平均總價元':[df['總價元'].mean()], '總件數':[len(df)]})
    df['車位'] = df['交易筆棟數'].apply(lambda x:int(x[x.index('車位')+2:]))
    filter_b['總車位數'] = df['車位'].sum()
    filter_b['平均總價元(有車位)'] = df[df['車位']>0]['總價元'].mean()
    filter_b['平均車位總價元'] = df[df['交易標的']=='車位']['總價元'].mean()
    filter_b.to_csv('filter_b.csv', index = False, header=True)

if __name__ == '__main__':
    df = read_csv()
    # == filter_a ==
    export_a(df)
    # == filter_b ==
    export_b(df)