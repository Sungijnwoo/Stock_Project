import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import StockFunctions as sfs

data = sfs.GettingDailyDataFromDB('A027360')
priceDf = data['close']

mov5 = priceDf.rolling(5).mean()
mov20 = priceDf.rolling(20).mean()
print(mov5, mov20)





# df['ema5'] = df['Close'].ewm(5).mean()

# code = 'A027360'

# ma5_price = get_movingaverage(code, 5)   # 5일 이동평균가
# ma10_price = get_movingaverage(code, 10) # 10일 이동평균가

# print("5일선 : " + ma5_price, "10일선 : " + ma10_price)
