import pandas as pd
import os

df = pd.read_excel("네이버뉴스_테마관련.xlsx")
for x, i in enumerate(df['time']):
    for y, j in enumerate(i):
        if j.isdigit():
            df['time'][x] = i[y:y+8]
            break   

for x, i in enumerate(df['time']):
    try:
        if len(str(i)) > 8:
            df['time'][x] = str(i)[:8]
    except:
        pass

idx_num_l = []
for x, i in enumerate(df['time']):
    try:
        if not i.isdigit():
            idx_num_l += x,
    except:
        pass
df = df.drop(idx_num_l)
        
folder_path = os.getcwd()
xlsx_file_name = '네이버뉴스_테마.xlsx'
df.to_excel(xlsx_file_name, index=False)

print('엑셀 저장 완료 | 경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))

os.startfile(folder_path)