from sklearn.linear_model import LinearRegression #mean square error사용하는방법
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
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
 

Stock_code = ['075970']
Stock_code2 = ['U201']
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

    
    len = objStockChart.GetHeaderValue(3)
    
    for i in range(len):

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
    print(df)

    kda_open,kda_high,kda_low,kda_close,kda_amount = [],[],[],[],[]

    #코스닥 조회
    objStockChart.SetInputValue(0, 'U201') 
    objStockChart.SetInputValue(1, ord('2')) # 개수로 조회
    objStockChart.SetInputValue(4, 1) # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0,1,2,3,4,5,8,9]) #날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('m')) # '차트 주가 - 일간 차트 요청
    objStockChart.SetInputValue(7, 3)
    objStockChart.SetInputValue(9, ord('1')) # 수정주가 사용
    objStockChart.BlockRequest()

    len = objStockChart.GetHeaderValue(3)
    
    for i in range(len):
        kda_open.append(objStockChart.GetDataValue(2, i))
        kda_high.append(objStockChart.GetDataValue(3, i))
        kda_low.append(objStockChart.GetDataValue(4, i))
        kda_close.append(objStockChart.GetDataValue(5, i))
        kda_amount.append(objStockChart.GetDataValue(7, i))

    dict2 = {'kda_open' : kda_open, 'kda_high' : kda_high, 'kda_low' : kda_low, \
    'kda_close' : kda_close, 'kda_amount' : kda_amount}


    df1 = pd.DataFrame(dict2, columns=['kda_open','kda_high','kda_low','kda_close','kda_amount'])
    df1.sort_index(ascending=False)
    #print(df1)
    

    name_list = ['kda_open','kda_high','kda_low','kda_close','kda_amount']
    value_list = [kda_open,kda_high,kda_low,kda_close,kda_amount]

    for x,i in enumerate(value_list):   
        df['{}'.format(name_list[x])] = i
    
    print(df)
    
    ksi_open,ksi_high,ksi_low,ksi_close,ksi_amount = [],[],[],[],[]

    #코스피 조회
    objStockChart.SetInputValue(0, 'U001') 
    objStockChart.SetInputValue(1, ord('2')) # 개수로 조회
    objStockChart.SetInputValue(4, 1) # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0,1,2,3,4,5,8,9]) #날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('m')) # '차트 주가 - 일간 차트 요청
    objStockChart.SetInputValue(7, 3)
    objStockChart.SetInputValue(9, ord('1')) # 수정주가 사용
    objStockChart.BlockRequest()

    len = objStockChart.GetHeaderValue(3)
    
    for i in range(len):
        ksi_open.append(objStockChart.GetDataValue(2, i))
        ksi_high.append(objStockChart.GetDataValue(3, i))
        ksi_low.append(objStockChart.GetDataValue(4, i))
        ksi_close.append(objStockChart.GetDataValue(5, i))
        ksi_amount.append(objStockChart.GetDataValue(7, i))

    dict3 = {'ksi_open' : ksi_open, 'ksi_high' : ksi_high, 'ksi_low' : ksi_low, \
    'ksi_close' : ksi_close, 'ksi_amount' : ksi_amount}


    df2 = pd.DataFrame(dict3, columns=['ksi_open','ksi_high','ksi_low','ksi_close','ksi_amount'])
    df2.sort_index(ascending=False)
    #print(df2)

    name_list2 = ['ksi_open','ksi_high','ksi_low','ksi_close','ksi_amount']
    value_list2 = [ksi_open,ksi_high,ksi_low,ksi_close,ksi_amount]

    for x,i in enumerate(value_list2):   
        df['{}'.format(name_list2[x])] = i
    
    print(df)
    df.head()


    day_list = []
    time_list = []
    open_list = []
    high_list = []
    low_list = []
    close_list = []
    compare_list = []
    vol_list = []
    amount_list = []



# compare_data = pd.read_excel('동국알앤에스_test_Data.xlsx')
# compare_data.drop(['compare','day','time'], axis=1, inplace=True)
# print(compare_data.shape)

# test_model = joblib.load('testdata.pkl')

# y_compare_predict = test_model.predict(compare_data)

# print(y_compare_predict)
