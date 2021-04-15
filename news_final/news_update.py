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

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
 
myToken = "xoxb-1902032357250-1925843516096-ntzh70Shz2QOjx9BKSDpKmJ3"
def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    post_message(myToken,"#stock", strbuf)

interest_news = ["스푸트니크", "아주ib투자", "한화솔루션", "동국알앤에스"]
past_url = ['', '', '', '']

text_model = joblib.load('text_model.pkl') 
title_model = joblib.load('title_model.pkl') 
text_tdif = joblib.load('text_transformer.pkl')
title_tdif = joblib.load('title_transformer.pkl')
text_cv = joblib.load('text_vectorizer.pkl') 
title_cv = joblib.load('title_vectorizer.pkl') 

    

print('브라우저를 실행시킵니다(자동 제어)\n')
browser = webdriver.Chrome(r"D:\4_1\Stock_Project\naver_news_crawling\chromedriver.exe")
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

        # search_opt_box = browser.find_element_by_xpath('//*[@id="snb"]/div[1]/div/div[1]/a[2]')
        # search_opt_box.click()

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
            dbgout("{} 관련 뉴스 : {}".format(interest_news[i], title))
            print(":", title)
            input = title_cv.transform(title)
            input = title_tdif.transform(input)
            output = title_model.predict(input)
            if output == 1:
                print("{} 주식 무조건 오름".format(interest_news[i]))
            else:
                print("{} 주식 무조건 떨어짐".format(interest_news[i]))
            print("")
        browser.refresh()
    cnt += 1
    if cnt == 100:
        break
    

        




        