import win32com.client
import pandas as pd
import os 

day_list = []
time_list = []
open_list = []
high_list = []
low_list = []
close_list = []
compare_list = []
vol_list = []
amount_list = []
# 연결 여부 체크

Stock_code = ['052460', '093230', '003530', '041190', '005257', '043610', '075970', '144510', '246690', '066910', '194480', '241840', '031390', '094480', '100790', '086890', '006280', '021080', '118990', '237690', '086980', '128940', '309930', '053030', '307930', '027830', '024810', '067730', '274090', '035720', '049470', '000910', '246960', '027360', '019550', '071055', '064260', '086520', '247540', '089980', '042510', '203650', '042600', '241520', '087260', '297570', '066970', '053280', '208350', '008930', '071050', '005250', '096040', '089150', '137400', '020150', '036030', '192250', '016450', '052600', '217600', '314930', '003535', '289220', '004270', '217270', '003670']
Stock_name = ['아이크래프트', '이아이디', '한화투자증권', '우리기술투자', '녹십자홀딩스2우', '지니뮤직', '동국알앤에스', '녹십자랩셀', 'TS인베스트먼트', '손오공', '데브시스터즈', '에이스토리', '녹십자셀', '갤럭시아머니트리', '미래에셋벤처투자', '이수앱지스', '녹십자', '에이티넘인베스트', '모트렉스', '에스티팜', '쇼박스', '한미약품', '오하임아이엔티', '바이넥스', '컴퍼니케이', '대성창투', '이화전기', '로지시스', '켄코아에어로스페이스', '카카오', 'SGA', '유니온', '이노테라피', '아주IB투자', 'SBI인베스트 먼트', '한국금융지주우', '다날', '에코프로', '에코프로비엠', '상아프론테크', '라온시큐어', '드림시큐리티', '새로닉스', 'DSC인베스트먼트', '모바일어플라이언스', '알로이스', '엘앤에프', '예스24', '지란지교시큐리티', '한미사이언스', '한국금융지주', '녹십자홀딩스', '이트론', '케이씨티', '피엔티', '일진머티리얼즈', 'KTH', '케이사인', '한세예스24홀딩스', '한네트', '켐온', '바이오다인', '한화투자증권우', '자이언트스텝', '남성', '넵튠', '포스코케미칼']

for i in range(len(Stock_code)):
    Stock_code[i] = Stock_code[i].replace("A","")

objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
 

# 차트 객체 구하기
for x,j in enumerate(Stock_code):
    objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    objStockChart.SetInputValue(0, "A" + j)   #종목 코드 - 아주IB투자
    objStockChart.SetInputValue(1, ord('2')) # 개수로 조회
    objStockChart.SetInputValue(4, 2000) # 하루 381개 0900 ~ 1520
    objStockChart.SetInputValue(5, [0,1,2,3,4,5,6, 8,9]) #날짜,시간,시가,고가,저가,종가,전일대비,거래량,거래대금
    objStockChart.SetInputValue(6, ord('D')) # '차트 주가 - 일간 차트 요청
    objStockChart.SetInputValue(9, ord('1')) # 수정주가 사용
    objStockChart.BlockRequest()

    
    len = objStockChart.GetHeaderValue(3)
    
    print("날짜","시간", "시가", "고가", "저가", "종가", "거래량","거래대금")
    print("빼기빼기==============================================-")

    for i in range(len):

        day_list.append(objStockChart.GetDataValue(0, i))
        time_list.append(objStockChart.GetDataValue(1, i))
        open_list.append(objStockChart.GetDataValue(2, i))
        high_list.append(objStockChart.GetDataValue(3, i))
        low_list.append(objStockChart.GetDataValue(4, i))
        close_list.append(objStockChart.GetDataValue(5, i))
        compare_list.append(objStockChart.GetDataValue(6, i))
        vol_list.append(objStockChart.GetDataValue(7, i))
        amount_list.append(objStockChart.GetDataValue(8, i))
    dict1 = {'day' : day_list, 'time' : time_list, 'open' : open_list, 'high' : high_list, 'low' : low_list, \
    'close' : close_list,'compare' : compare_list, 'vol' : vol_list, 'amount' : amount_list}


    df = pd.DataFrame(dict1, columns=['day','time','open','high','low','close','compare','vol','amount'])
    df.sort_index(ascending=False)
    # print(df)
    day_list = []
    time_list = []
    open_list = []
    high_list = []
    low_list = []
    close_list = []
    compare_list = []
    vol_list = []
    amount_list = []

    #df2 =pd.DataFrame(index=range(0,Stock_len), columns=['mov5','ema5','mov10','ema10','mov20','ema20','mov60','ema60','mov120','ema120'])
    # df2 =pd.DataFrame(index=range(0,df.shape[0]), columns=['blank'])
    # df2 = df2.drop(['blank'], axis = 1)


    # df2['mov5'] = df['close'].rolling(5).mean() #단순이동평균
    # df2['ema5'] = df['close'].ewm(5).mean() #지수 이동평균 - 최근값에 가중치를 두면서 계산
    # df2['mov10'] = df['close'].rolling(10).mean()
    # df2['ema10'] = df['close'].ewm(10).mean()
    # df2['mov20'] = df['close'].rolling(20).mean()
    # df2['ema20'] = df['close'].ewm(20).mean()
    # df2['mov60'] = df['close'].rolling(60).mean()
    # df2['ema60'] = df['close'].ewm(60).mean()
    # df2['mov120'] = df['close'].rolling(120).mean()
    # df2['ema120'] = df['close'].ewm(120).mean()
    #print(df2)



    folder_path = os.getcwd()
    df.to_excel('{}_data_Day.xlsx'.format(Stock_name[x]))
    # df2.to_excel('IB_moving_average_Day.xlsx')
    os.startfile(folder_path)
