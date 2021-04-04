import sys, os
import requests
import selenium
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pickle, progressbar, json, glob, time
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys
###### 날짜 저장 ##########


sleep_sec = 0.5


####### 언론사별 본문 위치 태그 파싱 함수 ###########
print('본문 크롤링에 필요한 함수를 로딩하고 있습니다...\n' + '-' * 100)

def crawling_main_text(url):
    try:
        req = requests.get(url=url, timeout = 3)
    except:
        return None
    # req.encoding = None
    soup = BeautifulSoup(req.text, 'html.parser')
    
    # 연합뉴스
    if ('yna' in url) | ('app.yonhapnews' in url):
        main_article = soup.find('article', {'class':'story-news article'})
        if main_article == None:
            main_article = soup.find('article', {'class' : 'article-txt'})

        text = main_article.text
        time = soup.find('p', {'class' : 'update-time'}).text
        # time = time[4:14]

    elif 'econonews' in url:
        text = soup.find('div', {'class' : 'cont-body'}).text
        time = soup.find('span', {'class' : 'info'}).text
        # time = time[9:19]
    
    elif 'itooza' in url:
        text = soup.find('div', {'id' : 'article-body'}).text
        time = soup.find('span', {'class' : 'date'}).text
        # time = time[:8]
    
    elif 'sedaily' in url:
        text = soup.find('div', {'class' : 'article_view'}).text
        time = soup.find('span', {'class' : 'url_txt'}).text
        # time = time[2:12]

    elif 'edaily' in url: 
        text = soup.find('div', {'class' : 'news_body'}).text
        time = soup.find('div', {'class' : 'dates'}).text

    elif 'mrepublic' in url:
        text = soup.find('div', {'class' : 'article-body'}).text
        time = soup.find('div', {'class' : 'info-group'}).text
        # time = time[4:14]
    
    elif 'gukjenews' in url:
        text = soup.find('div', {'class' : 'article-body'}).text
        time = soup.find('div', {'class' : 'info-group'}).text

    elif 'heraldcorp' in url:
        text = soup.find('div', {'id' : 'articleText'}).text
        time = soup.find('li', {'class' : 'article_date'}).text

    elif 'moneys.mt' in url:
        text = soup.find('div', {'id' : 'article'}).text
        time = soup.find('span', {'class' : 'num'}).text
        # time = time[0:10]

    elif 'edaily.co' in url:
        text = soup.find('div', {'class' : 'news_body'}).text
        time = soup.find('div', {'class' : 'dates'}).text
    
    elif 'view.asiae.co' in url:
        text = soup.find('div', {'class' : 'article fb-quotable'}).text
        time = soup.find('p', {'class' : 'user_data'}).text

    elif 'businesspost.co' in url:
        text = soup.find('div', {'style' : 'text-align: justify;'}).text
        time = soup.find('div', {'class' : 'rn_sdate'}).text
    
    elif 'ggilbo.com' in url:
        text = soup.find('article', {'id' : 'article-view-content-div'}).text
        time = soup.find('ul', {'class' : 'infomation'}).text

    elif 'news1.kr' in url: 
        text = soup.find('div', {'class' : 'detail sa_area'}).text
        time = soup.find('ul', {'class' : 'article_info'}).text

    elif 'news.g-enews' in url:
        text = soup.find('div', {'class' : 'vtxt detailCont'}).text
        time = soup.find('p', {'class' : 'r3'}).text

    elif 'hankyung' in url:
        text = soup.find('div', {'id' : 'articletxt'}).text
        time = soup.find('div', {'class' : 'date_info'}).text
    
    elif 'fntoday' in url:
        text = soup.find('div', {'id' : 'article-view-content-div'}).text
        time = soup.find('div', {'class' : 'info-text'}).text

    elif 'thebell' in url:
        text = soup.find('div', {'class' : 'viewSection'}).text
        time = soup.find('span', {'class' : 'date'}).text

    elif 'todaykorea' in url:
        text = soup.find('div', {'id' : 'article-view-content-div'}).text
        time = soup.find('i', {'class' : 'icon-clock-o'}).text

    elif 'fnnews' in url:
        text = soup.find('div', {'id' : 'article_content'}).text
        time = soup.find('div', {'class' : 'byline'}).text

    elif 'biz.chosun' in url:
        text = soup.find('div', {'id' : 'news_body_id'}).text
        time = soup.find('div', {'class' : 'news_date'}).text
    
    elif 'news.mt' in url:
        text = soup.find('div', {'id' : 'textBody'}).text
        time = soup.find('div', {'class' : 'info'}).text

    elif 'ajunews' in url:
        text = soup.find('div', {'id' : 'articleBody'}).text
        time = soup.find('span', {'class' : 'date'}).text

    elif 'pinpointnews' in url:
        text = soup.find('div', {'class' : 'vc_con'}).text
        time = soup.find('p', {'class' : 'w1'}).text

    elif 'pinpointnews' in url:
        text = soup.find('div', {'class' : 'vc_con'}).text
        time = soup.find('p', {'class' : 'w1'}).text

    elif 'm-i' in url:
        text = soup.find('div', {'id' : 'article-view-content-div'}).text
        time = soup.find('div', {'class' : 'info-text'}).text

    # MBC 
    elif '//imnews.imbc' in url: 
        text = soup.find('div', {'itemprop' : 'articleBody'}).text
        time = soup.find('span', {'class' : 'input'}).text  
        # time = time.strip()
        # time = time[3:13]      

    # 매일경제, req.encoding = None 설정 필요
    elif 'mk.co' in url:
        main_article = soup.find('div', {'class' : 'art_txt'})
        if not main_article:
            main_article = soup.find('div', {'class' : 'view_txt'})
        text = main_article.text
        time = soup.find('li', {'class' : 'lasttime'}).text
        # time = time.strip()
        # time = time[5:15]
  
    # SBS
    elif 'news.sbs' in url:
        main_article = soup.find('div', {'itemprop' : 'articleBody'})
        if not main_article:
            main_article = soup.find('div', {'class' : 'article_cont_area'})
        text = main_article.text
        time = soup.find('span', {'class' : 'date'}).text
        # time = time[3:14]

    # KBS
    elif 'news.kbs' in url:
        text = soup.find('div', {'id' : 'cont_newstext'}).text
        time = soup.find('em', {'class': 'date'}).text
        # time = time[3:13]
    
    # JTBC
    elif 'news.jtbc' in url:
        text = soup.find('div', {'class' : 'article_content'}).text
        time = soup.find('span', {'class': 'i_date'}).text
        # time = time[3:13]
        
    # 그 외
    else:
        text = None
        time = None

    return text.replace('\n','').replace('\r','').replace('<br>','').replace('\t',''), time.replace('/', '').replace('-','').replace('.','')
    
# press_list = ['MBC']
# press_list = ['연합뉴스','KBS','매일경제','MBC','SBS','JTBC']

# print('검색할 언론사 : {} | {}개 \n'.format(press_list, len(press_list)))


# ############### 브라우저를 켜고 검색 키워드 입력 ####################
data = pd.read_excel("code_KOSDAQ.xlsx")
queries = data.loc[:, "name"]
queries = ["두산인프라코어", "바이넥스", "진양산업", "우리기술투자", "라온시큐어",
            "알로이스", "케이씨티"]
news_num = int(input('수집 뉴스의 수(숫자만 입력) : '))

print('\n' + '=' * 100 + '\n')

print('브라우저를 실행시킵니다(자동 제어)\n')
browser = webdriver.Chrome(r"G:\git_stock\Stock_Project\naver_news_crawling\chromedriver.exe")
print('\n크롤링을 시작합니다.')


for query in queries:
    news_dict = {}
    print(query + ' 추출중')
    pbar = tqdm(total=news_num)
    idx = 0
    news_url = 'https://search.naver.com/search.naver?where=news&query={}'.format(query)
    browser.get(news_url)
    time.sleep(2)

    ################ 뉴스 크롤링 ########################
    # ####동적 제어로 페이지 넘어가며 크롤링
    cur_page = 1     

    while cur_page < 400:
        table = browser.find_element_by_xpath('//ul[@class="list_news"]')
        li_list = table.find_elements_by_xpath('./li[contains(@id, "sp_nws")]')
        area_list = [li.find_element_by_xpath('.//div[@class="news_area"]') for li in li_list]
        a_list = [area.find_element_by_xpath('.//a[@class="news_tit"]') for area in area_list]
        for n in a_list:
            try:
                n_url = n.get_attribute('href')
                content, date = crawling_main_text(n_url)
                news_dict[idx] = {'company' : query, 
                                'title' : n.get_attribute('title'), 
                                'url' : n_url,
                                'time' : date,
                                'text' : content}
                idx += 1
                pbar.update(1)
                if idx == news_num:
                    break
            except:
                pass
        
        if idx < news_num:
            cur_page +=1
            try:
                elem = browser.find_element_by_class_name('btn_next')
                elem.send_keys(Keys.RETURN)
            except:
                break
            # try:
            #     pages = browser.find_element_by_xpath('//div[@class="sc_page_inner"]')
            #     next_page_url = [p for p in pages.find_elements_by_xpath('.//a') if p.text == str(cur_page)][0].get_attribute('href')
            # except:
            #     time.sleep(2)
            #     break
            # browser.get(next_page_url)
            time.sleep(sleep_sec)

        else:            
            # print('\n브라우저를 종료합니다.\n' + '=' * 100)
            time.sleep(2)
            # browser.close()
            break

    pbar.close()

#### 데이터 전처리하기 ###################################################### 

    print('데이터프레임 변환\n')
    news_df = pd.DataFrame(news_dict).T

    folder_path = os.getcwd()
    xlsx_file_name = '네이버뉴스_본문_{}개_{}.xlsx'.format(news_num, query)
    news_df.to_excel(xlsx_file_name)

    print('엑셀 저장 완료 | 경로 : {}\\{}\n'.format(folder_path, xlsx_file_name))

    os.startfile(folder_path)

    print('=' * 100 + '\n결과물의 일부')
    news_df