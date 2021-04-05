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
 

#Stock_name = input("차트 조회 종목코드 입력 : ")
#Stock_len = input("조회할 차트 수 입력 : ")
#Stock_len = 2000
Stock_code = ['053270', '009830','144510','075970','042670', '042510','053030','065350','052460','027360','297570','052420','041190','086890',
            '003780','089150','052600','048410','189980']
Stock_name = ["구영테크", "한화솔루션", "녹십자렙셀", "동국알앤에스", "두산인프라코어", "라온시큐어",
        "바이넥스", "신성델타테크", "아이크래프트", "아주ib투자", "알로이스", "오성첨단소재",
        "우리기술투자", "이수앱지스", "진양산업", "케이씨티", "한네트", "현대바이오",
        "흥국에프엔비"]
#toDate = input("마지막날짜 : ")
#fromDate = input("시작날짜 : ")
#toDate = 210405
#fromDate = 160405

# 차트 객체 구하기
for x,j in enumerate(Stock_code):
    objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    objStockChart.SetInputValue(0, "A" + j)   #종목 코드 - 아주IB투자
    objStockChart.SetInputValue(1, ord('2')) # 개수로 조회
    #objStockChart.SetInputValue(1, ord('1'))
    #objStockChart.SetInputValue(2, toDate)
    #objStockChart.SetInputValue(3, fromDate) # 위 1,2,3은 기간별 조회시 사용
    objStockChart.SetInputValue(4, 2000) # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0,1,2,3,4,5,6, 8,9]) #날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('D')) # '차트 주가 - 일간 차트 요청
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
        compare_list.append(objStockChart.GetDataValue(6, i))
        vol_list.append(objStockChart.GetDataValue(7, i))
        amount_list.append(objStockChart.GetDataValue(8, i))
    dict1 = {'day' : day_list, 'time' : time_list, 'open' : open_list, 'high' : high_list, 'low' : low_list, \
    'close' : close_list,'compare' : compare_list, 'vol' : vol_list, 'amount' : amount_list}


    df = pd.DataFrame(dict1, columns=['day','time','open','high','low','close','compare','vol','amount'])
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

    #df2 =pd.DataFrame(index=range(0,Stock_len), columns=['mov5','ema5','mov10','ema10','mov20','ema20','mov60','ema60','mov120','ema120'])
    df2 =pd.DataFrame(index=range(0,df.shape[0]), columns=['blank'])
    df2 = df2.drop(['blank'], axis = 1)


    df2['mov5'] = df['close'].rolling(5).mean() #단순이동평균
    df2['ema5'] = df['close'].ewm(5).mean() #지수 이동평균 - 최근값에 가중치를 두면서 계산
    df2['mov10'] = df['close'].rolling(10).mean()
    df2['ema10'] = df['close'].ewm(10).mean()
    df2['mov20'] = df['close'].rolling(20).mean()
    df2['ema20'] = df['close'].ewm(20).mean()
    df2['mov60'] = df['close'].rolling(60).mean()
    df2['ema60'] = df['close'].ewm(60).mean()
    df2['mov120'] = df['close'].rolling(120).mean()
    df2['ema120'] = df['close'].ewm(120).mean()
    #print(df2)



    folder_path = os.getcwd()
    df.to_excel('{}_data_Day.xlsx'.format(Stock_name[x]))
    # df2.to_excel('IB_moving_average_Day.xlsx')
    os.startfile(folder_path)
