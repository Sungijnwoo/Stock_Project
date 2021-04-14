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
folder_path = os.getcwd()

#리스트 생성
cur = []    #종가
base = []   #기준가
vol = []    #거래량
totOffer = []   #총매도잔량
totBid = []    #총매수잔량
off_10 = []    #10차 매도 호가틱 * 잔량
bid_10 = []    #10차 매수 호가틱 * 잔량
sum_10 = []    #off_10+bid_10
h_unit = []    #호가 단위
max_off = []    #최대 매도층
max_bid = []    #최대 매수층



def hoga(b):
    if b< 1000:
        r = 1
    elif b<5000:
        r = 5
    elif b<10000:
        r = 10
    elif b<50000:
        r = 50
    elif b<100000:
        r = 100
    elif b<500000:
        r = 500
    else: r = 1000
    return r

for i, c in enumerate(codeList):
    objStockMst.SetInputValue(0, c)
    ret = objStockMst.BlockRequest()
    if objStockMst.GetDibStatus() != 0:
        print("통신상태", objStockMst.GetDibStatus(), objStockMst.GetDibMsg1())
        break

    base.append(objStockMst.GetHeaderValue(27))
    vol.append(objStockMst.GetHeaderValue(18))
    totOffer.append(objStockMst.GetHeaderValue(71))
    totBid.append(objStockMst.GetHeaderValue(73))
    h_unit.append(hoga(base[i]))
    cur.append((objStockMst.GetHeaderValue(11)-base[i])/h_unit[i])
    off = np.array([])
    bid = np.array([])
    n_off = np.array([])
    n_bid = np.array([])
    for j in range(10):
        n_off = np.append(n_off, objStockMst.GetDataValue(2, j))
        n_bid = np.append(n_bid, objStockMst.GetDataValue(3, j))
        off = np.append(off, (j+1) * n_off[j])
        bid = np.append(bid, (10-j) * n_bid[j])
    off_10.append(off.sum())
    bid_10.append(bid.sum())
    sum_10.append(off.sum()-bid.sum())
    max_bid.append(n_bid.argmax()+1)
    max_off.append(10-n_off.argmax())
    print(i)


df = pd.DataFrame({'base' : base, 'hoga unit': h_unit, 'volume' : vol, 'total offer' : totOffer, 'total bid' : totBid, 'offer_10' : off_10, 'bid_10' : bid_10, 'max offer' : max_off, 'max bid' : max_bid, 'sum_10' : sum_10, 'current' : cur},
                  columns=['base', 'hoga unit', 'volume', 'total offer', 'total bid', 'offer_10', 'bid_10', 'max offer', 'max bid', 'sum_10', 'current'])

df.to_excel('price_10_KOSPI.xlsx')
#리스트 초기화
cur = []    #종가
base = []   #기준가
vol = []    #거래량
totOffer = []   #총매도잔량
totBid = []    #총매수잔량
off_10 = []    #10차 매도 호가틱 * 잔량
bid_10 = []    #10차 매수 호가틱 * 잔량
sum_10 = []    #off_10+bid_10
h_unit = []    #호가 단위
max_off = []    #최대 매도층
max_bid = []    #최대 매수층

for i, c in enumerate(codeList):
    objStockMst.SetInputValue(0, c)
    ret = objStockMst.BlockRequest()
    if objStockMst.GetDibStatus() != 0:
        print("통신상태", objStockMst.GetDibStatus(), objStockMst.GetDibMsg1())
        break

    base.append(objStockMst.GetHeaderValue(27))
    vol.append(objStockMst.GetHeaderValue(18))
    totOffer.append(objStockMst.GetHeaderValue(71))
    totBid.append(objStockMst.GetHeaderValue(73))
    h = hoga(base[i])
    h = 100 if h > 100 else h
    h_unit.append(h)
    cur.append((objStockMst.GetHeaderValue(11)-base[i])/h_unit[i])
    off = np.array([])
    bid = np.array([])
    n_off = np.array([])
    n_bid = np.array([])
    for j in range(10):
        n_off = np.append(n_off, objStockMst.GetDataValue(2, j))
        n_bid = np.append(n_bid, objStockMst.GetDataValue(3, j))
        off = np.append(off, (j+1) * n_off[j])
        bid = np.append(bid, (10-j) * n_bid[j])
    off_10.append(off.sum())
    bid_10.append(bid.sum())
    sum_10.append(off.sum()-bid.sum())
    max_bid.append(n_bid.argmax()+1)
    max_off.append(10-n_off.argmax())
    print(i)


df2 = pd.DataFrame({'base' : base, 'hoga unit': h_unit, 'volume' : vol, 'total offer' : totOffer, 'total bid' : totBid, 'offer_10' : off_10, 'bid_10' : bid_10, 'max offer' : max_off, 'max bid' : max_bid, 'sum_10' : sum_10, 'current' : cur},
                  columns=['base', 'hoga unit', 'volume', 'total offer', 'total bid', 'offer_10', 'bid_10', 'max offer', 'max bid', 'sum_10', 'current'])

df2.to_excel('price_10_KOSDAQ.xlsx')
os.startfile(folder_path)