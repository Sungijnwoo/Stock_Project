import re

def preprocessing(text):
    # 개행문자 제거
    text = re.sub('\\\\n', ' ', text)
    # 특수문자 제거
    # 특수문자나 이모티콘 등은 때로는 의미를 갖기도 하지만 여기에서는 제거했습니다.
    text = re.sub('[?.,;:|\)*~`’!^\-_+<>@\#$%&-=#}※]', '', text)
    # 한글, 영문, 숫자만 남기고 모두 제거하도록 합니다.
    text = re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9]', ' ', text)
    # 한글, 영문만 남기고 모두 제거하도록 합니다.
    text = re.sub('[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z]', ' ', text)
    # 중복으로 생성된 공백값을 제거합니다.
    text = re.sub(' +', ' ', text)
    return text

# 불용어 제거
def remove_stopwords(text):
    tokens = text.split(' ')
    stops = ['수', '현', '있는', '있습니다', '그', '년도', '합니다', '하는', 
             '및', '제', '할', '하고', '더', '대한', '한', '그리고', '월', 
             '저는', '없는', '입니다', '등', '일', '많은', '이런', '것은', 
             '왜','같은', '같습니다', '없습니다', '위해', '한다', '특징주', 
             'STOCK', '단독', '파이낸스', 'activate', 'javascript', 'for',
             'chosun', '제휴안내', '구독신청', 'biz', 'co', 'kr', 'copyright',
             'com', 'asiae', 'fnnews', 'facebook', 'written', 'share', '카카오톡',
             '네이버', '블로그', '주소', '복사', '크랩', '댓글', '무단전재',
             '배포', '금지', '다른', '뉴스', "  ", "facebooktwittershare카카오톡카카오톡네이버블로그네이버블로그주소복사",
             "facebooktwittershare카카오톡카카오톡네이버블로그네이버블로그주소복사", "이미지주소복사스크랩댓글please",
             "javascriptwrite", "athekpmcom", 'cbiz봇이', '기자기자', 'viewer', '주식', 'copyright 조선비즈', 'javascriptwrite',
             'javascript를', 'javascript를활성화해주세요', 'chosuncom제휴안내구독신청', 'cj', 'comment', 'in', '실시간으로', 'ai',
             '전문기업', '씽크풀과', "파이낸셜뉴스이", '블로그', '주소', '복사', '크랩', '댓글', '무단전재', '배포', '금지', '다른', '뉴스', "  ", "facebooktwittershare카카오톡카카오톡네이버블로그네이버블로그주소복사 이미지주소복사스크랩댓글please",
              "이미지주소복사스크랩댓글please","javascriptwrite", "athekpmcom", 'cbiz봇이', '기자기자', 'viewer', '주식', 'copyright 조선비즈', 'javascriptwrite',
             'javascript를', 'javascript를활성화해주세요', 'chosuncom제휴안내구독신청','cj', 'comment', 'in', '실시간으로', 'ai', '전문기업', '씽크풀과',
             "파이낸셜뉴스의", "협업으로", "로봇기자가", "실시간", '배포', '금지', '다른', '뉴스', "  ", "이미지주소복사스크랩댓글please", 
             "이미지주소복사스크랩댓글please","javascriptwrite", "athekpmcom", 'cbiz봇이', '기자기자', 'viewer', '주식', 'copyright 조선비즈', 'javascriptwrite',
             'javascript를', 'javascript를활성화해주세요', 'chosuncom제휴안내구독신청','cj', 'comment', 'in', '실시간으로', 'ai', '전문기업', '씽크풀과',
             "파이낸셜뉴스의", "협업으로",'로봇기자가', '실시간으로', '생산한', '전문기업', '씽크풀과', "파이낸셜뉴스의", "협업으로", "로봇기자가", "실시간",
             '배포', '금지', '다른', '뉴스', "facebooktwittershare카카오톡카카오톡네이버블로그네이버블로그주소복사 이미지주소복사스크랩댓글please", 
             "이미지주소복사스크랩댓글please","javascriptwrite", "athekpmcom", 'cbiz봇이', '기자기자', 'viewer', '주식', 'copyright 조선비즈', 'javascriptwrite',
             'javascript를', 'javascript를활성화해주세요', 'chosuncom제휴안내구독신청','cj', 'comment', 'in', '실시간으로', 'ai', '전문기업', 
             '씽크풀과', "파이낸셜뉴스의", "협업으로",'로봇기자가', '실시간으로', '생산하는', '기사입니다', 'atm', 'atm수수료', "liveretoday", "주요뉴스"
             ,"mkcokr", "moneysmtcokr", "moneysmtcokr라이브리 작성을", "moneysmtcokr라이브리 작성을 활성화해주세요", "naver",
             ]
    meaningful_words = [w for w in tokens if not w.lower() in stops]
    return ' '.join(meaningful_words)