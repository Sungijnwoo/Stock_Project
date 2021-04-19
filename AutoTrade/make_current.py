import win32com.client
import pandas as pd

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")

kospi = pd.read_excel('price_10_KOSPI.xlsx')
current = []
kospi_c = kospi['code']
time = kospi['time']
for i, c in enumerate(kospi_c):
    objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    objStockChart.SetInputValue(0, c)  # 종목 코드 - 아주IB투자
    objStockChart.SetInputValue(1, ord('2'))  # 개수로 조회

    objStockChart.SetInputValue(4, 10)  # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 6, 8, 9])  # 날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('m'))
    objStockChart.SetInputValue(7, 3)
    objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용

    objStockChart.BlockRequest()
    for j in range(10):
        t = objStockChart.GetDataValue(1, j)
        if t == time[i]:
            current.append(objStockChart.GetDataValue(5, j))
            break

kospi['current'] = current

kosdaq = pd.read_excel('price_10_KOSDAQ.xlsx')
current = []
kosdaq_c = kospi['code']
time = kosdaq['time']
for i, c in enumerate(kosdaq_c):
    objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    objStockChart.SetInputValue(0, c)  # 종목 코드 - 아주IB투자
    objStockChart.SetInputValue(1, ord('2'))  # 개수로 조회

    objStockChart.SetInputValue(4, 10)  # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 6, 8, 9])  # 날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('m'))
    objStockChart.SetInputValue(7, 3)
    objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용

    objStockChart.BlockRequest()
    for j in range(10):
        t = objStockChart.GetDataValue(1, j)
        if t == time[i]:
            current.append(objStockChart.GetDataValue(5, j))
            break

kosdaq['current'] = current

kospi.to_excel('hoga_KOSPI.xlsx')
kosdaq.to_excel('hoga_KOSDAQ.xlsx')