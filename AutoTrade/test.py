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
# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
 

Stock_len = input("조회할 차트 수 입력 : ")
Stock_bong = input("조회할 차트 분봉 종류 : ")
# 차트 객체 구하기
objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
objStockChart.SetInputValue(0, 'A027360')   #종목 코드 - 아주IB투자
objStockChart.SetInputValue(1, ord('2')) # 개수로 조회
#objStockChart.SetInputValue(1, ord('1'))
#objStockChart.SetInputValue(2, toDate)
#objStockChart.SetInputValue(3, fromDate) # 위 1,2,3은 기간별 조회시 사용
objStockChart.SetInputValue(4, Stock_len) # 하루 381개 0900 ~ 1520
objStockChart.SetInputValue(5, [0,1,2,3,4,5,8,9]) #날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
objStockChart.SetInputValue(6, ord('m')) # '차트 주가 - 일간 차트 요청
objStockChart.SetInputValue(7, Stock_bong)
objStockChart.SetInputValue(9, ord('1')) # 수정주가 사용
objStockChart.BlockRequest()
 
len = objStockChart.GetHeaderValue(3)
 
print("날짜","시간", "시가", "고가", "저가", "종가", "거래량","거래대금")
print("빼기빼기==============================================-")

for i in range(len):
    # day = objStockChart.GetDataValue(0, i)
    # time = objStockChart.GetDataValue(1, i)
    # open = objStockChart.GetDataValue(2, i)
    # high = objStockChart.GetDataValue(3, i)
    # low = objStockChart.GetDataValue(4, i)
    # close = objStockChart.GetDataValue(5, i)
    # vol = objStockChart.GetDataValue(6, i)
    # amount = objStockChart.GetDataValue(7, i)
    # print (day, time, open, high, low, close, vol,amount)

    day_list.append(objStockChart.GetDataValue(0, i))
    time_list.append(objStockChart.GetDataValue(1, i))
    open_list.append(objStockChart.GetDataValue(2, i))
    high_list.append(objStockChart.GetDataValue(3, i))
    low_list.append(objStockChart.GetDataValue(4, i))
    close_list.append(objStockChart.GetDataValue(5, i))
    vol_list.append(objStockChart.GetDataValue(6, i))
    amount_list.append(objStockChart.GetDataValue(7, i))
dict1 = {'day' : day_list, 'time' : time_list, 'open' : open_list, 'high' : high_list, 'low' : low_list, \
'close' : close_list, 'vol' : vol_list, 'amount' : amount_list}

df = pd.DataFrame(dict1, columns=['day','time','open','high','low','close','vol','amount'])
df.sort_index(ascending=False)
print(df)




