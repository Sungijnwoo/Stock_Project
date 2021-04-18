type_of_news = {
    "크래프톤" : ["오하임아이엔티", "대성창투", "아주IB투자", "넵튠", "이노테라피", "TS인베스트먼트"],
    "야놀자" : ["SBI인베스트 먼트", "아주IB투자"],
    "카카오뱅크" : ["예스24", "한세예스24홀딩스", "드림시큐리티", "한국금융지주우", "한국금융지주", "카카오"],
    "두나무" : ["에이티넘인베스트", "대성창투", "우리기술투자", "한화투자증권우", "한화투자증권", "다날"],
    "2차전지" : ["엘앤에프", "일진머티리얼즈", "포스코케미칼", "에코프로", "새로닉스", "에코프로비엠", "상아프론테크", "피엔티"],
    "백신여권" : ["아이크래프트", "라온시큐어", "지란지교시큐리티", "SGA"],
    "CMO" : ["한미사이언스", "한미약품", "녹십자랩셀", "녹십자홀딩스", "녹십자셀", "녹십자홀딩스2우", "녹십자", "바이넥스", "에스티팜", "켐온"],
    "스푸트니크" : ["이트론", "이수앱지스", "바이넥스", "이아이디", "이화전기", "데브시스터즈", "바이오다인"],
    "디지털화폐" : ['케이사인', '로지시스', '케이씨티', '한네트', "켄코아에어로스페이스", "갤럭시아머니트리"],
    "OTT" : ['손오공', '알로이스', '에이스토리', '쇼박스', '지니뮤직'],
    "메타버스" : ['모트렉스', '모바일어플라이언스', '남성', '자이언트스텝'],
    "미중갈등" : ['동국알앤에스', '유니온']
}

import pandas as pd
import os
import datetime
# import holidays
import numpy as np

news = []
for i in type_of_news.values():
    news += i
df = pd.read_excel("네이버뉴스_테마.xlsx")

df_list = []
df_y_label = []
kr_holidays = holidays.KR()
for new in news:
    df_list.append(pd.read_excel("{}_data_Day.xlsx".format(new)))


for x, y in zip(df['company'], df['time']):
    updown = 0
    length = len(type_of_news[x])
    for i in type_of_news[x]:
        pos = news.index(i)
        try:
            today = datetime.datetime.strptime(str(y), "%Y%m%d").date()
            while today in kr_holidays or today.weekday() >= 5 or (today.month == 12 and today.day == 31):
                today = today + datetime.timedelta(1)
            yesterday = today - datetime.timedelta(1)
            while yesterday in kr_holidays or yesterday.weekday() >= 5 or (yesterday.month == 12 and yesterday.day == 31):
                yesterday = yesterday - datetime.timedelta(1)
            today = int(str(today).replace("-", ""))
            yesterday = int(str(yesterday).replace("-", ""))
            today_high = int(df_list[pos][df_list[pos]['day'] == today]['close'])
            yesterday_close = int(df_list[pos][df_list[pos]['day'] == yesterday]['close'])
            updown += (today_high - yesterday_close) / yesterday_close * 100
        except:
            break
    # print(today_high, yesterday_close)
    # print(updown)
    df_y_label.append(float(updown) / length)




df['rate'] = df_y_label

folder_path = os.getcwd()
xlsx_file_name = '네이버뉴스_본문_테마관련_rate.xlsx'
df.to_excel(xlsx_file_name, index=False)

print('엑셀 저장 완료 | 경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))

os.startfile(folder_path)
