import sys, os
import requests
import selenium
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pickle, json, glob, time
from sklearn.feature_extraction.text import CountVectorizer
from selenium.webdriver.common.keys import Keys
from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd
from datetime import datetime
import time, calendar
import requests
from crawling import crawling_main_text
from remove_stopword import preprocessing, remove_stopwords

def post_message(token, channel, text):
    requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
 
myToken = "xoxb-1902032357250-1925843516096-ntzh70Shz2QOjx9BKSDpKmJ3"
def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    post_message(myToken,"#stock", strbuf)

interest_news = ["이재명", "윤석열", "진단키트", "오세훈", "코로나", "스푸트니크", "CMO", "반도체", "2차전지", "미중갈등", "희토류", "조바이든 저탄소", "이트론"]
past_url = ['' for i in interest_news]

text_model = joblib.load(r'C:\git-project\Stock_Project\news_final\models\text_model.pkl') 
title_model = joblib.load(r'C:\git-project\Stock_Project\news_final\models\title_model.pkl') 
text_tdif = joblib.load(r'C:\git-project\Stock_Project\news_final\models\text_transformer.pkl')
title_tdif = joblib.load(r'C:\git-project\Stock_Project\news_final\models\title_transformer.pkl')
text_cv = joblib.load(r'C:\git-project\Stock_Project\news_final\models\text_vectorizer.pkl') 
title_cv = joblib.load(r'C:\git-project\Stock_Project\news_final\models\title_vectorizer.pkl') 

    

print('브라우저를 실행시킵니다(자동 제어)\n')
browser = webdriver.Chrome(r"C:\git-project\Stock_Project\naver_news_crawling\chromedriver.exe")
for i in range(len(interest_news) - 1):
    browser.execute_script('window.open("about:blank", "_blank");')
tabs = browser.window_handles

print('\n크롤링을 시작합니다.')


for x, new in enumerate(interest_news):
    news_url = 'https://search.naver.com/search.naver?where=news&query={}'.format(new)
    # TAB_1
    browser.switch_to_window(tabs[x])
    browser.get(news_url)

for i in range(len(interest_news)):
    browser.switch_to_window(tabs[i])
    search_opt_box = browser.find_element_by_xpath('//*[@id="snb"]/div[1]/div/div[1]/a[2]')
    search_opt_box.click()

    table = browser.find_element_by_xpath('//ul[@class="list_news"]')
    li_list = table.find_elements_by_xpath('./li[contains(@id, "sp_nws")]')
    area_list = [li.find_element_by_xpath('.//div[@class="news_area"]') for li in li_list]
    a_list = [area.find_element_by_xpath('.//a[@class="news_tit"]') for area in area_list]
    n = a_list[0]
    n_url = n.get_attribute('href')

    past_url[i] = n_url

cnt = 0
while True:
    for i in range(len(interest_news)):
        browser.switch_to_window(tabs[i])

        table = browser.find_element_by_xpath('//ul[@class="list_news"]')
        li_list = table.find_elements_by_xpath('./li[contains(@id, "sp_nws")]')
        area_list = [li.find_element_by_xpath('.//div[@class="news_area"]') for li in li_list]
        a_list = [area.find_element_by_xpath('.//a[@class="news_tit"]') for area in area_list]
        n = a_list[0]
        n_url = n.get_attribute('href')

        if past_url[i] != n_url:
            print("{}시 {}분 {} 새로운 뉴스 발견".format(datetime.now().hour, datetime.now().minute, interest_news[i]))
            past_url[i] = n_url
            title = [n.get_attribute('title')]
            print(":", title)
            title[0] = preprocessing(title[0])
            title[0] = remove_stopwords(title[0])
            title_input = title_cv.transform(title)
            title_input = title_tdif.transform(title_input)
            title_output = title_model.predict_proba(title_input)
            dbgout("{} 관련 뉴스 제목 : {}".format(interest_news[i], title))
            print("title proba", title_output)

            # try:
            #     text, date = crawling_main_text(n_url)
            #     text = [preprocessing(text)]
            #     text[0] = remove_stopwords(text[0])
            #     text_input = text_cv.transform(text)
            #     text_input = text_tdif.transform(text_input)
            #     text_output = text_model.predict_proba(text_input)
            #     dbgout("{} 관련 뉴스 내용 : {}".format(interest_news[i], text))
            #     print("text proba", text_output)
            # except:
            #     pass           
            
        browser.refresh()
    # cnt += 1
    # if cnt == 100:
    #     break
    

        




        