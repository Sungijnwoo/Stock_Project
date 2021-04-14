import win32com.client
type_of_news = {
    "크래프톤" : ["오하임아이엔티", "대성창투", "아주IB투자", "넵튠", "이노테라피", "TS인베스트먼트"],
    "야놀자" : ["SBI인베스트먼트", "아주IB투자", "DSC인베스트먼트"],
    "카카오뱅크" : ["예스24", "한세예스24홀딩스", "드림시큐리티", "한국금융지주우", "한국금융지주", "카카오"],
    "리디북스" : ["컴퍼니케이", "에이티넘인베스트", "미래에셋벤처투자", "대성창투"],
    "두나무" : ["에이티넘인베스트", "대성창투", "우리기술투자", "한화투자증권우", "한화투자증권", "다날"],
    "2차전지" : ["엘앤에프", "일진머티리얼즈", "포스코케미칼", "에코프로", "새로닉스", "에코프로비엠", "상아프론테크", "피엔티"],
    "백신여권" : ["아이크래프트", "라온시큐어", "지란지교시큐리티", "SGA"],
    "CMO" : ["한미사이언스", "한미약품", "녹십자랩셀", "녹십자홀딩스", "녹십자셀", "녹십자홀딩스2우", "녹십자", "바이넥스", "에스티팜", "켐온"],
    "스푸트니크" : ["이트론", "이수앱지스", "바이넥스", "이아이디", "이화전기", "데브시스터즈", "바이오다인"],
    "디지털화폐" : ['케이사인', '로지시스', '케이씨티', '한네트', "켄코아에어로스페이스", "갤럭시아머니트리"],
    "ott" : ['손오공', '알로이스', 'KTH', '에이스토리', '쇼박스', '지니뮤직'],
    "메타버스" : ['모트렉스', '모바일어플라이언스', '남성', '자이언트스텝'],
    "미중갈등" : ['동국알앤에스', '유니온']
}
code_list = []
name_list = []
for i in type_of_news.values():
    name_list += i

name_list = list(set(name_list))

print(name_list)


# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()
 
# 종목코드 리스트 구하기
objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = objCpCodeMgr.GetStockListByMarket(1) #거래소
codeList2 = objCpCodeMgr.GetStockListByMarket(2) #코스닥

codeList_Entire = codeList + codeList2
find = 0
for i in name_list:
    for j in codeList_Entire:
        if i == objCpCodeMgr.CodeToName(j):
            code_list += j,
            #print(j,i)
            find = 1
    if find == 0:
        print(i)
    find = 0
print(code_list)