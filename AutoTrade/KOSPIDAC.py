from pandas_datareader import data
from datetime import datetime

s_date = datetime(2006,1,1)
e_date = datetime(2021,4,1)

df = data.get_data_yahoo("^KS11",s_date,e_date)
#print("날짜", "고가", "저가", "시초가", "종가", "거래량","수정주가")
print(df)