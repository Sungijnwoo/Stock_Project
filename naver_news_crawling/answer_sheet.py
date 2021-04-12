import pandas as pd
import os
import datetime
import holidays
import numpy as np

df = pd.read_excel("네이버뉴스_본문_22000.xlsx")
news = ["구영테크", "한화솔루션", "녹십자렙셀", "동국알앤에스", "두산인프라코어", "라온시큐어",
        "바이넥스", "신성델타테크", "아이크래프트", "아주ib투자", "알로이스", "오성첨단소재",
        "우리기술투자", "이수앱지스", "진양산업", "케이씨티", "한네트", "현대바이오",
        "흥국에프엔비", "HMM"]
df_list = []
df_y_label = []
kr_holidays = holidays.KR()
for new in news:
    df_list.append(pd.read_excel("일봉_뉴스_답/{}_data_Day.xlsx".format(new)))

for x, y in zip(df['company'], df['time']):
    if x == "그린뉴딜": x = "한화솔루션"
    pos = news.index(x)
    
    try:
        today = datetime.datetime.strptime(str(y), "%Y%m%d").date()
        while today in kr_holidays or today.weekday() >= 5 or (today.month == 12 and today.day == 31):
            today = today + datetime.timedelta(1)
        yesterday = today - datetime.timedelta(1)
        while yesterday in kr_holidays or yesterday.weekday() >= 5 or (yesterday.month == 12 and yesterday.day == 31):
            yesterday = yesterday - datetime.timedelta(1)
        today = int(str(today).replace("-", ""))
        yesterday = int(str(yesterday).replace("-", ""))
        today_high = int(df_list[pos][df_list[pos]['day'] == today]['high'])     
        yesterday_close = int(df_list[pos][df_list[pos]['day'] == yesterday]['close'])
    except:
        df_y_label.append(np.nan)
        continue
    # print(today_high, yesterday_close)
    df_y_label.append((today_high - yesterday_close) / yesterday_close * 100
    )




df['rate'] = df_y_label

folder_path = os.getcwd()
xlsx_file_name = '네이버뉴스_본문_22000.xlsx'
df.to_excel(xlsx_file_name, index=False)

print('엑셀 저장 완료 | 경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))

os.startfile(folder_path)
