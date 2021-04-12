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
interest_news = ["두산인프라코어", "아주ib투자"]
past_url = ['', '']

text_model = joblib.load('text_model.pkl') 
title_model = joblib.load('title_model.pkl') 
# with open('text_model.pkl', 'rb') as f:  # cv.pkl이라는 파일을 바이너리 읽기(rb)모드로 열어서 f라 하고
#     text_model = pickle.load(f) 
# with open('title_model.pkl', 'rb') as f:  # cv.pkl이라는 파일을 바이너리 읽기(rb)모드로 열어서 f라 하고
#     title_model = pickle.load(f) 
with open('text_train_feature_vector.pkl', 'rb') as f:  # cv.pkl이라는 파일을 바이너리 읽기(rb)모드로 열어서 f라 하고
    text_cv = pickle.load(f) 
with open('title_train_feature_vector.pkl', 'rb') as f:  # cv.pkl이라는 파일을 바이너리 읽기(rb)모드로 열어서 f라 하고
    title_cv = pickle.load(f) 

# print('브라우저를 실행시킵니다(자동 제어)\n')
# browser = webdriver.Chrome(r"D:\4_1\Stock_Project\naver_news_crawling\chromedriver.exe")
# for i in range(len(interest_news) - 1):
#     browser.execute_script('window.open("about:blank", "_blank");')
# tabs = browser.window_handles

# print('\n크롤링을 시작합니다.')


# for x, new in enumerate(interest_news):
#     news_url = 'https://search.naver.com/search.naver?where=news&query={}'.format(new)
#     # TAB_1
#     browser.switch_to_window(tabs[x])
#     browser.get(news_url)

# cnt = 0
# while True:
#     for i in range(len(interest_news)):
#         browser.switch_to_window(tabs[i])

#         search_opt_box = browser.find_element_by_xpath('//*[@id="main_pack"]/div[1]/div[1]/a[2]')
#         search_opt_box.click()

#         table = browser.find_element_by_xpath('//ul[@class="list_news"]')
#         li_list = table.find_elements_by_xpath('./li[contains(@id, "sp_nws")]')
#         area_list = [li.find_element_by_xpath('.//div[@class="news_area"]') for li in li_list]
#         a_list = [area.find_element_by_xpath('.//a[@class="news_tit"]') for area in area_list]
#         n = a_list[0]
#         n_url = n.get_attribute('href')
#         if past_url[i] != n_url:
#             print("{} 새로운 뉴스 발견".format(interest_news[i]))
#             past_url[i] = n_url
#             title = n.get_attribute('title')
#             print(":", title)
#             # input = cv.transform(title)
#             # output = news_model.fit(input)
#         browser.refresh()
#     cnt += 1
#     if cnt == 20:
#         break
    

        




        