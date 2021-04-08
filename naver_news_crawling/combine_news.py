import pandas as pd
import os
news = ["구영테크", "그린뉴딜", "녹십자렙셀", "동국알앤에스", "두산인프라코어", "라온시큐어",
        "라온시큐어", "바이넥스", "신성델타테크", "아이크래프트", "아주ib투자", "알로이스", "오성첨단소재",
        "우리기술투자", "이수앱지스", "진양산업", "케이씨티", "한네트", "한화솔루션", "현대바이오",
        "흥국에프엔비"]

df = pd.read_excel("네이버뉴스_본문_1000개_HMM.xlsx")

for new in news:
    tmp = pd.read_excel("네이버뉴스_본문_1000개_{}.xlsx".format(new))
    df = pd.concat([df, tmp])

df = df.drop(['Unnamed: 0'], axis=1)
folder_path = os.getcwd()
xlsx_file_name = '네이버뉴스_본문_22000.xlsx'
df.to_excel(xlsx_file_name, index=False)

print('엑셀 저장 완료 | 경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))

os.startfile(folder_path)