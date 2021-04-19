from sklearn.linear_model import LinearRegression #mean square error사용하는방법
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
import win32com.client
import os
import numpy as np


move_num = [5,20,60,120]

objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
 

#Stock_code = ['075970','005930','052460']
#Stock_name = ["동국알앤에스","삼성전자","아이크래프트"]
Stock_code = ['075970']
Stock_name = ["동국알앤에스"]


for x,j in enumerate(Stock_code):
    objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    objStockChart.SetInputValue(0, "A" + j) 
    objStockChart.SetInputValue(1, ord('2')) # 개수로 조회
    objStockChart.SetInputValue(4, 1) # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0,1,2,3,4,5,8,9]) #날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('m')) # '차트 주가 - 일간 차트 요청
    objStockChart.SetInputValue(7, 3)
    objStockChart.SetInputValue(9, ord('1')) # 수정주가 사용
    objStockChart.BlockRequest()

    
    leng = objStockChart.GetHeaderValue(3)

    day_list = []
    time_list = []
    open_list = []
    high_list = []
    low_list = []
    close_list = []
    compare_list = []
    vol_list = []
    amount_list = []
    
    for i in range(leng):

        open_list.append(objStockChart.GetDataValue(2, i))
        high_list.append(objStockChart.GetDataValue(3, i))
        low_list.append(objStockChart.GetDataValue(4, i))
        close_list.append(objStockChart.GetDataValue(5, i))
        vol_list.append(objStockChart.GetDataValue(6, i))
        amount_list.append(objStockChart.GetDataValue(7, i))
    dict1 = {'open' : open_list, 'high' : high_list, 'low' : low_list, \
    'close' : close_list,'vol' : vol_list, 'amount' : amount_list}


    df = pd.DataFrame(dict1, columns=['open','high','low','close','vol','amount'])
    df.sort_index(ascending=False)
    #print(df)

    #코스닥 조회

    kda_open,kda_high,kda_low,kda_close,kda_amount,kda_close_move,kda_amount_move,price_moving_tmp, amount_moving_tmp = [],[],[],[],[],[],[],[],[]

    objStockChart.SetInputValue(0, 'U201') 
    objStockChart.SetInputValue(1, ord('2')) # 개수로 조회
    objStockChart.SetInputValue(4, 120) # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0,1,2,3,4,5,8,9]) #날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('m')) # '차트 주가 - 일간 차트 요청
    objStockChart.SetInputValue(7, 3)
    objStockChart.SetInputValue(9, ord('1')) # 수정주가 사용
    objStockChart.BlockRequest()

    
    kda_open.append(objStockChart.GetDataValue(2, 0))
    kda_high.append(objStockChart.GetDataValue(3, 0))
    kda_low.append(objStockChart.GetDataValue(4, 0))
    kda_close.append(objStockChart.GetDataValue(5, 0))
    kda_amount.append(objStockChart.GetDataValue(7, 0))

    for j in move_num:
        for i in range(j):
            kda_close_move.append(objStockChart.GetDataValue(5, i))
            kda_amount_move.append(objStockChart.GetDataValue(7, i))

        kda_close_numpy = np.array(kda_close_move)
        kda_amount_numpy = np.array(kda_amount_move)
        price_moving_tmp += int(np.mean(kda_close_numpy)),
        amount_moving_tmp += int(np.mean(kda_amount_numpy)),
        
        kda_close_move, kda_amount_move= [], []

    # feature_list = ['price_5_moving','price_20_moving','price_60_moving','price_120_moving','amount_5_moving','amount_20_moving','amount_60_moving','amount_120_moving']
    # tmp_list = price_moving_tmp + amount_moving_tmp
    feature_list = ['kda_amount_5_moving','kda_amount_20_moving','kda_amount_60_moving','kda_amount_120_moving']
    tmp_list = amount_moving_tmp

    name_list1 = ['kda_open','kda_high','kda_low','kda_close','kda_amount']
    value_list1 = [kda_open,kda_high,kda_low,kda_close,kda_amount]


    for x,i in enumerate(tmp_list):
        value_list1 += i,
        name_list1 += '{}'.format(feature_list[x]),



    #코스피 조회

    ksi_open,ksi_high,ksi_low,ksi_close,ksi_amount,ksi_close_move,ksi_amount_move,price_moving_tmp, amount_moving_tmp = [],[],[],[],[],[],[],[],[]

    objStockChart.SetInputValue(0, 'U001') 
    objStockChart.SetInputValue(1, ord('2')) # 개수로 조회
    objStockChart.SetInputValue(4, 120) # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0,1,2,3,4,5,8,9]) #날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('m')) # '차트 주가
    objStockChart.SetInputValue(7, 3)
    objStockChart.SetInputValue(9, ord('1')) # 수정주가 사용
    objStockChart.BlockRequest()

    
    ksi_open.append(objStockChart.GetDataValue(2, 0))
    ksi_high.append(objStockChart.GetDataValue(3, 0))
    ksi_low.append(objStockChart.GetDataValue(4, 0))
    ksi_close.append(objStockChart.GetDataValue(5, 0))
    ksi_amount.append(objStockChart.GetDataValue(7, 0))

    for j in move_num:
        for i in range(j):
            ksi_close_move.append(objStockChart.GetDataValue(5, i))
            ksi_amount_move.append(objStockChart.GetDataValue(7, i))

        ksi_close_numpy = np.array(ksi_close_move)
        ksi_amount_numpy = np.array(ksi_amount_move)
        price_moving_tmp += int(np.mean(ksi_close_numpy)),
        amount_moving_tmp += int(np.mean(ksi_amount_numpy)),
        
        ksi_close_move, ksi_amount_move= [], []

    # feature_list = ['price_5_moving','price_20_moving','price_60_moving','price_120_moving','amount_5_moving','amount_20_moving','amount_60_moving','amount_120_moving']
    # tmp_list = price_moving_tmp + amount_moving_tmp
    feature_list = ['ksi_amount_5_moving','ksi_amount_20_moving','ksi_amount_60_moving','ksi_amount_120_moving']
    tmp_list = amount_moving_tmp

    name_list2 = ['ksi_open','ksi_high','ksi_low','ksi_close','ksi_amount']
    value_list2 = [ksi_open,ksi_high,ksi_low,ksi_close,ksi_amount]


    for x,i in enumerate(tmp_list):
        value_list2 += i,
        name_list2 += '{}'.format(feature_list[x]),

    #코스피 코스닥 feature 합치기 

    name_list = name_list1 + name_list2
    value_list = value_list1 + value_list2

    #print(len(name_list))
    #print(len(value_list))

    # df에 추가하기 

    for x,i in enumerate(value_list):
        df['{}'.format(name_list[x])] = i
    
    print(df)

    test_model = joblib.load('testdata.pkl')
    y_predict = test_model.predict(df)
    print(y_predict)




# compare_data = pd.read_excel('동국알앤에스_test_Data.xlsx')
# compare_data.drop(['compare','day','time'], axis=1, inplace=True)


# test_model = joblib.load('testdata.pkl')

# y_compare_predict = test_model.predict(compare_data.iloc[0])

# print(y_compare_predict)
