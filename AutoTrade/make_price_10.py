import win32com.client
import pandas as pd
import numpy as np
import os

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

# c = 'A027360'  # 아주IB투자

# 종목코드 리스트 구하기
objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = objCpCodeMgr.GetStockListByMarket(1)  # 거래소
codeList2 = objCpCodeMgr.GetStockListByMarket(2)  # 코스닥
objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
folder_path = os.getcwd()

# 리스트 생성
code = []  # 종목 코드
time = []  # 시간
base = []  # 기준가
vol = []  # 거래량
totOffer = []  # 총매도잔량
totBid = []  # 총매수잔량
off_10 = []
off_9 = []
off_8 = []
off_7 = []
off_6 = []
off_5 = []
off_4 = []
off_3 = []
off_2 = []
off_1 = []  # 10차 매도 호가 잔량
bid_1 = []
bid_2 = []
bid_3 = []
bid_4 = []
bid_5 = []
bid_6 = []
bid_7 = []
bid_8 = []
bid_9 = []
bid_10 = []  # 10차 매수 호가 잔량
sum_10 = []  # off_10+bid_10
h_unit = []  # 호가 단위


def hoga(b):
    if b < 1000:
        r = 1
    elif b < 5000:
        r = 5
    elif b < 10000:
        r = 10
    elif b < 50000:
        r = 50
    elif b < 100000:
        r = 100
    elif b < 500000:
        r = 500
    else:
        r = 1000
    return r


for i, c in enumerate(codeList):
    objStockMst.SetInputValue(0, c)

    objStockChart.SetInputValue(0, c)  # 종목 코드 - 아주IB투자
    objStockChart.SetInputValue(1, ord('2'))  # 개수로 조회
    # objStockChart.SetInputValue(1, ord('1'))
    # objStockChart.SetInputValue(2, toDate)
    # objStockChart.SetInputValue(3, fromDate) # 위 1,2,3은 기간별 조회시 사용
    objStockChart.SetInputValue(4, 1)  # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 6, 8, 9])  # 날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('m'))
    objStockChart.SetInputValue(7, 3)
    objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
    ret = objStockMst.BlockRequest()
    objStockChart.BlockRequest()
    if objStockMst.GetDibStatus() != 0:
        print("통신상태", objStockMst.GetDibStatus(), objStockMst.GetDibMsg1())
        break

    code.append(c)
    time.append(objStockChart.GetDataValue(1, 0))
    base.append(objStockChart.GetDataValue(2, 0))
    vol.append(objStockMst.GetHeaderValue(18))
    totOffer.append(objStockMst.GetHeaderValue(71))
    totBid.append(objStockMst.GetHeaderValue(73))
    h_unit.append(hoga(base[i]))

    n_off = np.array([])
    n_bid = np.array([])
    for j in range(10):
        n_off = np.append(n_off, objStockMst.GetDataValue(2, j))
        n_bid = np.append(n_bid, objStockMst.GetDataValue(3, j))

    off_10.append(n_off[9])
    off_9.append(n_off[8])
    off_8.append(n_off[7])
    off_7.append(n_off[6])
    off_6.append(n_off[5])
    off_5.append(n_off[4])
    off_4.append(n_off[3])
    off_3.append(n_off[2])
    off_2.append(n_off[1])
    off_1.append(n_off[0])
    bid_1.append(n_bid[0])
    bid_2.append(n_bid[1])
    bid_3.append(n_bid[2])
    bid_4.append(n_bid[3])
    bid_5.append(n_bid[4])
    bid_6.append(n_bid[5])
    bid_7.append(n_bid[6])
    bid_8.append(n_bid[7])
    bid_9.append(n_bid[8])
    bid_10.append(n_bid[9])
    sum_10.append(n_off.sum() - n_bid.sum())

    print(i)

df = pd.DataFrame(
    {'code': code, 'time': time, 'base': base, 'hoga unit': h_unit, 'volume': vol, 'total offer': totOffer,
     'total bid': totBid,
     'offer_10': off_10, 'offer_9': off_9, 'offer_8': off_8, 'offer_7': off_7, 'offer_6': off_6, 'offer_5': off_5,
     'offer_4': off_4, 'offer_3': off_3, 'offer_2': off_2, 'offer_1': off_1,
     'bid_1': bid_1, 'bid_2': bid_2, 'bid_3': bid_3, 'bid_4': bid_4, 'bid_5': bid_5, 'bid_6': bid_6, 'bid_7': bid_7,
     'bid_8': bid_8, 'bid_9': bid_9, 'bid_10': bid_10, 'sum_10': sum_10},
    columns=['code', 'time', 'base', 'hoga unit', 'volume', 'total offer', 'total bid', 'offer_10', 'offer_9',
             'offer_8', 'offer_7', 'offer_6', 'offer_5', 'offer_4', 'offer_3', 'offer_2', 'offer_1',
             'bid_1', 'bid_2', 'bid_3', 'bid_4', 'bid_5', 'bid_6', 'bid_7', 'bid_8', 'bid_9', 'bid_10', 'sum_10'])

df.to_excel('price_10_KOSPI.xlsx')
# 리스트 초기화
code = []  # 종목 코드
time = []  # 시간
base = []  # 기준가
vol = []  # 거래량
totOffer = []  # 총매도잔량
totBid = []  # 총매수잔량
off_10 = []
off_9 = []
off_8 = []
off_7 = []
off_6 = []
off_5 = []
off_4 = []
off_3 = []
off_2 = []
off_1 = []  # 10차 매도 호가 잔량
bid_1 = []
bid_2 = []
bid_3 = []
bid_4 = []
bid_5 = []
bid_6 = []
bid_7 = []
bid_8 = []
bid_9 = []
bid_10 = []  # 10차 매수 호가 잔량
sum_10 = []  # off_10+bid_10
h_unit = []  # 호가 단위

for i, c in enumerate(codeList):
    objStockMst.SetInputValue(0, c)
    objStockChart.SetInputValue(0, c)  # 종목 코드 - 아주IB투자
    objStockChart.SetInputValue(1, ord('2'))  # 개수로 조회
    # objStockChart.SetInputValue(1, ord('1'))
    # objStockChart.SetInputValue(2, toDate)
    # objStockChart.SetInputValue(3, fromDate) # 위 1,2,3은 기간별 조회시 사용
    objStockChart.SetInputValue(4, 1)  # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 6, 8, 9])  # 날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('m'))
    objStockChart.SetInputValue(7, 3)
    objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
    ret = objStockMst.BlockRequest()
    objStockChart.BlockRequest()
    if objStockMst.GetDibStatus() != 0:
        print("통신상태", objStockMst.GetDibStatus(), objStockMst.GetDibMsg1())
        break

    code.append(c)
    time.append(objStockChart.GetDataValue(1, 0))
    base.append(objStockChart.GetDataValue(2, 0))
    vol.append(objStockMst.GetHeaderValue(18))
    totOffer.append(objStockMst.GetHeaderValue(71))
    totBid.append(objStockMst.GetHeaderValue(73))
    h = hoga(base[i])
    h = 100 if h > 100 else h
    h_unit.append(h)
    n_off = np.array([])
    n_bid = np.array([])
    for j in range(10):
        n_off = np.append(n_off, objStockMst.GetDataValue(2, j))
        n_bid = np.append(n_bid, objStockMst.GetDataValue(3, j))

    off_10.append(n_off[9])
    off_9.append(n_off[8])
    off_8.append(n_off[7])
    off_7.append(n_off[6])
    off_6.append(n_off[5])
    off_5.append(n_off[4])
    off_4.append(n_off[3])
    off_3.append(n_off[2])
    off_2.append(n_off[1])
    off_1.append(n_off[0])
    bid_1.append(n_bid[0])
    bid_2.append(n_bid[1])
    bid_3.append(n_bid[2])
    bid_4.append(n_bid[3])
    bid_5.append(n_bid[4])
    bid_6.append(n_bid[5])
    bid_7.append(n_bid[6])
    bid_8.append(n_bid[7])
    bid_9.append(n_bid[8])
    bid_10.append(n_bid[9])
    sum_10.append(n_off.sum() - n_bid.sum())
    print(i)

df2 = pd.DataFrame(
    {'code': code, 'time': time, 'base': base, 'hoga unit': h_unit, 'volume': vol, 'total offer': totOffer,
     'total bid': totBid,
     'offer_10': off_10, 'offer_9': off_9, 'offer_8': off_8, 'offer_7': off_7, 'offer_6': off_6, 'offer_5': off_5,
     'offer_4': off_4, 'offer_3': off_3, 'offer_2': off_2, 'offer_1': off_1,
     'bid_1': bid_1, 'bid_2': bid_2, 'bid_3': bid_3, 'bid_4': bid_4, 'bid_5': bid_5, 'bid_6': bid_6, 'bid_7': bid_7,
     'bid_8': bid_8, 'bid_9': bid_9, 'bid_10': bid_10, 'sum_10': sum_10},
    columns=['code', 'time', 'base', 'hoga unit', 'volume', 'total offer', 'total bid', 'offer_10', 'offer_9',
             'offer_8', 'offer_7', 'offer_6', 'offer_5', 'offer_4', 'offer_3', 'offer_2', 'offer_1',
             'bid_1', 'bid_2', 'bid_3', 'bid_4', 'bid_5', 'bid_6', 'bid_7', 'bid_8', 'bid_9', 'bid_10', 'sum_10'])

df2.to_excel('price_10_KOSDAQ.xlsx')
os.startfile(folder_path)
