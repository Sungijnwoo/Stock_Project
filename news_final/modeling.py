import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
import pickle
import joblib

df = pd.read_excel('네이버뉴스_본문_22000_2.xlsx')

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
             '씽크풀과', "파이낸셜뉴스의", "협업으로",'로봇기자가', '실시간으로', '생산하는', '기사입니다', 'atm', 'atm수수료']
    meaningful_words = [w for w in tokens if not w.lower() in stops]
    return ' '.join(meaningful_words)

df = df.dropna(axis = 0)

df['title'] = df['title'].apply(preprocessing)
df['title'] = df['title'].apply(remove_stopwords)
df['text'] = df['text'].apply(preprocessing)
df['text'] = df['text'].apply(remove_stopwords)

df = df.reset_index(drop=True)

idx = []
for x,i in enumerate(df['text']):
  if len(i) < 100: idx.append(x)
df = df.drop(idx)

vectorizer = CountVectorizer(analyzer = 'word', # 캐릭터 단위로 벡터화 할 수도 있습니다.
                             tokenizer = None, # 토크나이저를 따로 지정해 줄 수도 있습니다.
                             preprocessor = None, # 전처리 도구
                             stop_words = None, # 불용어 nltk등의 도구를 사용할 수도 있습니다.
                             min_df = 2, # 토큰이 나타날 최소 문서 개수로 오타나 자주 나오지 않는 특수한 전문용어 제거에 좋습니다. 
                             ngram_range=(1, 3), # BOW의 단위를 1~3개로 지정합니다.
                             max_features = 2500 # 만들 피처의 수, 단어의 수가 됩니다.
                            )

title_train_feature_vector = vectorizer.fit_transform(df['title'])
text_train_feature_vector = vectorizer.fit_transform(df['text'])

joblib.dump(title_train_feature_vector, 'title_train_feature_vector.pkl')
joblib.dump(text_train_feature_vector, 'text_train_feature_vector.pkl')

title_transformer = TfidfTransformer(smooth_idf=False)
text_transformer = TfidfTransformer(smooth_idf=False)

title_train_feature_tfidf = title_transformer.fit_transform(title_train_feature_vector)
text_train_feature_tfidf = text_transformer.fit_transform(text_train_feature_vector)

joblib.dump(title_transformer, 'title_transformer.pkl')
joblib.dump(text_transformer, 'text_transformer.pkl')

X_title = title_train_feature_tfidf
X_text = text_train_feature_tfidf
Y = df.loc[:, 'updown']

X_train_title, X_test_title, y_train, y_test = train_test_split(X_title, Y, test_size=0.33, random_state=42)
X_train_text, X_test_text, y_train, y_test = train_test_split(X_text, Y, test_size=0.33, random_state=42)

forest_text = RandomForestClassifier(
    n_estimators = 100, n_jobs = -1, random_state=42)
forest_title = RandomForestClassifier(
    n_estimators = 100, n_jobs = -1, random_state=42)

forest_text = forest_text.fit(X_train_text, y_train)
forest_title = forest_title.fit(X_train_title, y_train)

joblib.dump(forest_text, 'text_model.pkl')
joblib.dump(forest_title, 'title_model.pkl')