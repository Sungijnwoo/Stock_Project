import win32com.client
import pandas as pd
import os

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

c = 'A027360'  # 아주IB투자

# 종목코드 리스트 구하기
objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = objCpCodeMgr.GetStockListByMarket(1)  # 거래소
codeList2 = objCpCodeMgr.GetStockListByMarket(2)  # 코스닥
objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")

# #리스트 생성
# cur = []    #종가
# base = []   #기준가
# vol = []    #거래량
# totOffer = []   #총매도잔량
# totBid = []    #총매수잔량
# off_10 = []    #(10차매도가-시가) * 잔량
# bid_10 = []    #(10차매수가-시가) * 잔량
# sum_10 = []    #off_10+bid_10
#

# for i, c in enumerate(codeList):
#     if i<1400:
#         continue
#     objStockMst.SetInputValue(0, c)
#     ret = objStockMst.BlockRequest()
#     if objStockMst.GetDibStatus() != 0:
#         print("통신상태", objStockMst.GetDibStatus(), objStockMst.GetDibMsg1())
#         break
#     cur.append(objStockMst.GetHeaderValue(11))
#     base.append(objStockMst.GetHeaderValue(27))
#     vol.append(objStockMst.GetHeaderValue(18))
#     totOffer.append(objStockMst.GetHeaderValue(71))
#     totBid.append(objStockMst.GetHeaderValue(73))
#     off = 0
#     bid = 0
#     for j in range(5):
#         off += (objStockMst.GetDataValue(0, j) - base[i-1400]) * objStockMst.GetDataValue(2, j)
#         bid += (objStockMst.GetDataValue(1, j) - base[i-1400]) * objStockMst.GetDataValue(3, j)
#     off_10.append(off/base[i-1400] if base[i-1400]!= 0 else 0)
#     bid_10.append(bid/base[i-1400] if base[i-1400]!= 0 else 0)
#     sum_10.append((off+bid)/base[i-1400] if base[i-1400]!= 0 else 0)
#     print(i)
#
#
# df = pd.DataFrame({'base' : base, 'volume' : vol, 'total offer' : totOffer, 'total bid' : totBid, 'offer_10' : off_10, 'bid_10' : bid_10, 'sum_10' : sum_10, 'current' : cur},
#                   columns=['base','volume', 'total offer', 'total bid', 'offer_10', 'bid_10', 'sum_10', 'current'])

#리스트 초기화
cur = []    #종가
base = []   #기준가
vol = []    #거래량
totOffer = []   #총매도잔량
totBid = []    #총매수잔량
off_10 = []    #(10차매도가-시가) * 잔량
bid_10 = []    #(10차매수가-시가) * 잔량
sum_10 = []    #off_10+bid_10

for i, c in enumerate(codeList2):
    objStockMst.SetInputValue(0, c)
    ret = objStockMst.BlockRequest()
    if objStockMst.GetDibStatus() != 0:
        print("통신상태", objStockMst.GetDibStatus(), objStockMst.GetDibMsg1())
        break
    cur.append(objStockMst.GetHeaderValue(11))
    base.append(objStockMst.GetHeaderValue(27))
    vol.append(objStockMst.GetHeaderValue(18))
    totOffer.append(objStockMst.GetHeaderValue(71))
    totBid.append(objStockMst.GetHeaderValue(73))
    off = 0
    bid = 0
    for j in range(5):
        off += (objStockMst.GetDataValue(0, j) - base[i]) * objStockMst.GetDataValue(2, j)
        bid += (objStockMst.GetDataValue(1, j) - base[i]) * objStockMst.GetDataValue(3, j)
    off_10.append(off/base[i] if base[i]!= 0 else 0)
    bid_10.append(bid/base[i] if base[i]!= 0 else 0)
    sum_10.append((off+bid)/base[i] if base[i]!= 0 else 0)
    print(i)

df2 = pd.DataFrame({'base' : base, 'volume' : vol, 'total offer' : totOffer, 'total bid' : totBid, 'offer_10' : off_10, 'bid_10' : bid_10, 'sum_10' : sum_10, 'current' : cur},
                  columns=['base','volume', 'total offer', 'total bid', 'offer_10', 'bid_10', 'sum_10', 'current'])

folder_path = os.getcwd()
# df.to_excel('price_10_KOSPI_7.xlsx')
df2.to_excel('price_5_KOSDAQ.xlsx')
os.startfile(folder_path)