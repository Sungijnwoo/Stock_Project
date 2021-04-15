import win32com.client
import pandas as pd
import os 

day_list = []
time_list = []
open_list = []
high_list = []
low_list = []
close_list = []
compare_list = []
vol_list = []
amount_list = []

objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
 

Stock_code = ['011200','052460']
Stock_name = ["HMM","아이크래프트"]


for x,j in enumerate(Stock_code):
    objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    objStockChart.SetInputValue(0, "A" + j)   #종목 코드 - 아주IB투자
    objStockChart.SetInputValue(1, ord('2')) # 개수로 조회
    objStockChart.SetInputValue(4, 10) # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0,1,2,3,4,5,8,9]) #날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('m')) # '차트 주가 - 일간 차트 요청
    objStockChart.SetInputValue(7, 3)
    objStockChart.SetInputValue(9, ord('1')) # 수정주가 사용
    objStockChart.BlockRequest()

    
    len = objStockChart.GetHeaderValue(3)
    
    for i in range(len):

        day_list.append(objStockChart.GetDataValue(0, i))
        time_list.append(objStockChart.GetDataValue(1, i))
        open_list.append(objStockChart.GetDataValue(2, i))
        high_list.append(objStockChart.GetDataValue(3, i))
        low_list.append(objStockChart.GetDataValue(4, i))
        close_list.append(objStockChart.GetDataValue(5, i))
        #compare_list.append(objStockChart.GetDataValue(6, i))
        vol_list.append(objStockChart.GetDataValue(6, i))
        amount_list.append(objStockChart.GetDataValue(7, i))
    dict1 = {'day' : day_list, 'time' : time_list, 'open' : open_list, 'high' : high_list, 'low' : low_list, \
    'close' : close_list,'vol' : vol_list, 'amount' : amount_list}


    df = pd.DataFrame(dict1, columns=['day','time','open','high','low','close','vol','amount'])
    df.sort_index(ascending=False)
    print(df)

    day_list = []
    time_list = []
    open_list = []
    high_list = []
    low_list = []
    close_list = []
    compare_list = []
    vol_list = []
    amount_list = []
