import selenium.webdriver.support.ui as ui
 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
 
#chromedriver 경로 설정
CHROMEDRIVER_PATH = './chromedriver.exe'
 
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
 
 
#브라우저 실행 및 탭 추가
driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options )
driver.execute_script('window.open("about:blank", "_blank");')
driver.execute_script('window.open("about:blank", "_blank");')
 
tabs = driver.window_handles
 
# TAB_1
driver.switch_to_window(tabs[0])
driver.get('http://www.naver.com/')
 
# TAB_2
driver.switch_to_window(tabs[1])
driver.get('http://www.google.com/')
 
# TAB_3
driver.switch_to_window(tabs[2])
driver.get('https://heodolf.tistory.com/')
