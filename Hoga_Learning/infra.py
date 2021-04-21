import win32com.client
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression

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

objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")

hoga_model = joblib.load('hoga_KOSPI_LR.pkl')
code = ['A075970', 'A005930', 'A052460']

for i, c in enumerate(code):
    df = []
    objStockMst.SetInputValue(0, c)
    ret = objStockMst.BlockRequest()
    if objStockMst.GetDibStatus() != 0:
        print("통신상태", objStockMst.GetDibStatus(), objStockMst.GetDibMsg1())
        break

    df.append(objStockMst.GetHeaderValue(11)) #base
    df.append(hoga(df[0])) #hoga unit
    df.append(objStockMst.GetHeaderValue(18)) #volume
    df.append(objStockMst.GetHeaderValue(71)) #total offer
    df.append(objStockMst.GetHeaderValue(73)) #total bid


    n_off = np.array([])
    n_bid = np.array([])
    for j in range(10):
        n_off = np.append(n_off, objStockMst.GetDataValue(2, j))
        n_bid = np.append(n_bid, objStockMst.GetDataValue(3, j))
    for j in range(9, -1, -1):
        df.append(n_off[j]) #offer_n
    for j in range(10):
        df.append(n_bid[j]) #bid_n

    df.append(n_off.sum() - n_bid.sum()) #sum_10
    df = np.array([df])
    df.reshape(1,-1)
    pred = hoga_model.predict(df)
    print(i, pred, df[0][0])