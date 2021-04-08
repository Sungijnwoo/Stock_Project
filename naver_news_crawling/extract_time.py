import pandas as pd
import os

news = ["라온시큐어", "알로이스"]

# for new in news:
#     a = pd.read_excel("네이버뉴스_본문_1000개_{}.xlsx".format(new))
#     for x, i in enumerate(a['time']):
#         for y, j in enumerate(i):
#             if j.isdigit():
#                 a['time'][x] = i[y:y+8]
#                 break

# for new in news:
#     a = pd.read_excel("네이버뉴스_본문_1000개_{}.xlsx".format(new))
#     for x, i in enumerate(a['time']):
#         try:
#             if len(str(i)) > 8:
#                 a['time'][x] = str(i)[:8]
#         except:
#             pass

for new in news:
    a = pd.read_excel("네이버뉴스_본문_1000개_{}.xlsx".format(new))
    # idx_num_l = []
    # for x, i in enumerate(a['time']):
    #     try:
    #         if not i.isdigit():
    #             idx_num_l += x,
    #     except:
    #         pass
    # a = a.drop(idx_num_l)
            
    # folder_path = os.getcwd()
    # xlsx_file_name = '네이버뉴스_본문_1000개_{}.xlsx'.format(new)
    # a.to_excel(xlsx_file_name, index=False)

    # print('엑셀 저장 완료 | 경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))

    # os.startfile(folder_path)