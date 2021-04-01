import win32com.client
import pandas as pd
import os

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

# 종목코드 리스트 구하기
objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = objCpCodeMgr.GetStockListByMarket(1)  # 거래소
codeList2 = objCpCodeMgr.GetStockListByMarket(2)  # 코스닥

code = []
name = []
for i, c in enumerate(codeList):
    code.append(c)
    name.append(objCpCodeMgr.CodeToName(c))

df = pd.DataFrame({'code' : code, 'name' : name}, columns=['code','name'])

code = []
name = []
for i, c in enumerate(codeList2):
    code.append(c)
    name.append(objCpCodeMgr.CodeToName(c))

df2 = pd.DataFrame({'code' : code, 'name' : name}, columns=['code','name'])

folder_path = os.getcwd()
df.to_excel('code_KOSPI.xlsx')
df2.to_excel('code_KOSDAQ.xlsx')
os.startfile(folder_path)