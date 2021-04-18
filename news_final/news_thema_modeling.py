import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
import pickle
import joblib
from remove_stopword import preprocessing, remove_stopwords
from imblearn.over_sampling import SMOTE
from sklearn.metrics import roc_auc_score, confusion_matrix, accuracy_score

df = pd.read_excel(r"C:\git-project\Stock_Project\news_final\테마관련주답\네이버뉴스_본문_테마관련_rate.xlsx")
df = df.dropna(axis = 0)

df['title'] = df['title'].apply(preprocessing)
df['title'] = df['title'].apply(remove_stopwords)
df['text'] = df['text'].apply(preprocessing)
df['text'] = df['text'].apply(remove_stopwords)

idx = df[(df['rate'] < 4) & (df['rate'] > -4)].index
df = df.drop(idx)

df['updown'] = np.where(df['rate']>0, 1, 0)

title_vectorizer = CountVectorizer(analyzer = 'word', # 캐릭터 단위로 벡터화 할 수도 있습니다.
                             tokenizer = None, # 토크나이저를 따로 지정해 줄 수도 있습니다.
                             preprocessor = None, # 전처리 도구
                             stop_words = ['ar', 'az', 'cbdc', 'ceo', 'cmo', 'db', 'esg', 'tv', 'vr', 'vs'], # 불용어 nltk등의 도구를 사용할 수도 있습니다.
                             min_df = 1, # 토큰이 나타날 최소 문서 개수로 오타나 자주 나오지 않는 특수한 전문용어 제거에 좋습니다. 
                             ngram_range=(1, 3), # BOW의 단위를 1~3개로 지정합니다.
                             max_features = 2000 # 만들 피처의 수, 단어의 수가 됩니다.
                            )
text_vectorizer = CountVectorizer(analyzer = 'word', # 캐릭터 단위로 벡터화 할 수도 있습니다.
                             tokenizer = None, # 토크나이저를 따로 지정해 줄 수도 있습니다.
                             preprocessor = None, # 전처리 도구
                             stop_words = ['ar', 'az', 'cbdc', 'ceo', 'cmo', 'db', 'esg', 'tv', 'vr', 'vs', 'vs청순', 'vs청순외계인이야', 'write', 'write택시기사', 'write택시기사 잘생겨서', 'liveretoday', 'liveretoday택시기사', 'liveretoday택시기사 잘생겨서', 'moneysmtcokr라이브리', 'moneysmtcokr라이브리 작성을', 'moneysmtcokr라이브리 작성을 활성화해주세요'], # 불용어 nltk등의 도구를 사용할 수도 있습니다.
                             min_df = 1, # 토큰이 나타날 최소 문서 개수로 오타나 자주 나오지 않는 특수한 전문용어 제거에 좋습니다. 
                             ngram_range=(1, 3), # BOW의 단위를 1~3개로 지정합니다.
                             max_features = 2000 # 만들 피처의 수, 단어의 수가 됩니다.
                            )


title_train_feature_vector = title_vectorizer.fit_transform(df['title'])
text_train_feature_vector = text_vectorizer.fit_transform(df['text'])

joblib.dump(title_vectorizer, 'cv_thema_title.pkl')
joblib.dump(text_vectorizer, 'cv_thema_text.pkl')

title_transformer = TfidfTransformer(smooth_idf=False)
text_transformer = TfidfTransformer(smooth_idf=False)

title_train_feature_tfidf = title_transformer.fit_transform(title_train_feature_vector)
text_train_feature_tfidf = text_transformer.fit_transform(text_train_feature_vector)

joblib.dump(title_transformer, 'tfid_thema_title.pkl')
joblib.dump(text_transformer, 'tfid_thema_text.pkl')


X_title = title_train_feature_tfidf
X_text = text_train_feature_tfidf
Y = df.loc[:, 'updown']

X_train_title, X_test_title, y_train_title, y_test_title = train_test_split(X_title, Y, test_size=0.33, random_state=42)
X_train_text, X_test_text, y_train_text, y_test_text = train_test_split(X_text, Y, test_size=0.33, random_state=42)

smote = SMOTE(random_state=13)
X_train_title_over,y_train_title_over = smote.fit_resample(X_train_title,y_train_title)
X_train_text_over,y_train_text_over = smote.fit_resample(X_train_text,y_train_text)


# 랜덤포레스트 분류기를 사용
lr_text = LogisticRegression(solver='lbfgs')
lr_title = LogisticRegression(solver='lbfgs')

lr_text = lr_text.fit(X_train_text_over, y_train_text_over)
lr_title = lr_title.fit(X_train_title_over, y_train_title_over)

joblib.dump(lr_text, 'model_thema_text.pkl')
joblib.dump(lr_title, 'model_thema_titla.pkl')

y_pred_text = lr_text.predict(X_test_text)
y_pred_title = lr_title.predict(X_test_title)

print("title_roc_auc_score : ", roc_auc_score(y_test_title, y_pred_title))
print("title_accuracy_score : ", accuracy_score(y_test_title, y_pred_title))

print("text_roc_auc_score : ", roc_auc_score(y_test_text, y_pred_text))
print("text_accuracy_score : ", accuracy_score(y_test_text, y_pred_text))


