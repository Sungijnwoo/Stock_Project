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

cur = 0    #종가
base = 0   #기준가
vol = 0    #거래량
totOffer = 0   #총매도잔량
totBid = 0    #총매수잔량
off_10 = 0    #(10차매도가-시가) * 잔량
bid_10 = 0    #(10차매수가-시가) * 잔량

objStockMst.SetInputValue(0, c)
ret = objStockMst.BlockRequest()
cur=(objStockMst.GetHeaderValue(11))
base=(objStockMst.GetHeaderValue(27))
vol=(objStockMst.GetHeaderValue(18))
totOffer=(objStockMst.GetHeaderValue(71))
totBid=(objStockMst.GetHeaderValue(73))
off = 0
bid = 0
for j in range(10):
    off += (objStockMst.GetDataValue(0, j) - base) * objStockMst.GetDataValue(2, j)
    bid += (objStockMst.GetDataValue(1, j) - base) * objStockMst.GetDataValue(3, j)
off_10=(off / base)
bid_10=(bid / base)

print(cur)
print(base)
print(vol)
print(totBid)
print(totOffer)
print(off_10)
print(bid_10)



# #리스트 생성
# cur = []    #종가
# base = []   #기준가
# vol = []    #거래량
# totOffer = []   #총매도잔량
# totBid = []    #총매수잔량
# off_10 = []    #(10차매도가-시가) * 잔량
# bid_10 = []    #(10차매수가-시가) * 잔량
#
#
# for i, c in enumerate(codeList):
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
#     for j in range(10):
#         off += (objStockMst.GetDataValue(0, j) - base[i]) * objStockMst.GetDataValue(2, j)
#         bid += (objStockMst.GetDataValue(1, j) - base[i]) * objStockMst.GetDataValue(3, j)
#     off_10.append(off/base[i])
#     bid_10.append(bid/base[i])
#
#
# df = pd.DataFrame({'base' : base, 'volume' : vol, 'total offer' : totOffer, 'total bid' : totBid, 'offer_10' : off_10, 'bid_10' : bid_10, 'current' : cur},
#                   columns=['base','volume', 'total offer', 'total bid', 'offer_10', 'bid_10', 'current'])

# #리스트 초기화
# cur = []    #종가
# base = []   #기준가
# vol = []    #거래량
# totOffer = []   #총매도잔량
# totBid = []    #총매수잔량
# off_10 = []    #(10차매도가-시가) * 잔량
# bid_10 = []    #(10차매수가-시가) * 잔량
#
# for i, c in enumerate(codeList2):
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
#     for j in range(10):
#         off += (objStockMst.GetDataValue(0, j) - base[i]) * objStockMst.GetDataValue(2, j)
#         bid += (objStockMst.GetDataValue(1, j) - base[i]) * objStockMst.GetDataValue(3, j)
#     off_10.append(off/base[i])
#     bid_10.append(bid/base[i])
#
#
# df2 = pd.DataFrame({'base' : base, 'volume' : vol, 'total offer' : totOffer, 'total bid' : totBid, 'offer_10' : off_10, 'bid_10' : bid_10, 'current' : cur},
#                   columns=['base','volume', 'total offer', 'total bid', 'offer_10', 'bid_10', 'current'])
#
# folder_path = os.getcwd()
# df.to_excel('price_10_KOSPI.xlsx')
# # df2.to_excel('price_10_KOSDAQ.xlsx')
# os.startfile(folder_path)