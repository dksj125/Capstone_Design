from selenium import webdriver
from selenium.common.exceptions import WebDriverException as WDE
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from Comment_Crawl import Comment_Crawl
from download_video import download_video

url = "https://youtube.com/"

keyword = input("검색: ")

finished_line = 10

path = "./chromedriver.exe"

browser = webdriver.Chrome(path)
browser.maximize_window()

browser.get(url)
time.sleep(2)

search = browser.find_element_by_name("search_query")
time.sleep(2)
search.send_keys(keyword)
search.send_keys(Keys.ENTER)

present_url = browser.current_url
browser.get(present_url)

last_page_height = browser.execute_script("return document.documentElement.scrollHeight")

while True:
    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)
    
    new_page_height = browser.execute_script("return document.documentElement.scrollHeight")
    
    if new_page_height > finished_line:
        break;
    
    else:
        last_page_height = new_page_height
        
        
html_source = browser.page_source

soup = BeautifulSoup(html_source, 'lxml')

test = soup.find_all("ytd-video-renderer", attrs={"class":'style-scope ytd-item-section-renderer'})

video_list = []

for i in test:
    
    title = i.find("yt-formatted-string", attrs={"class":'style-scope ytd-video-renderer'}).get_text()
    name = i.find("a", attrs={"class":'yt-simple-endpoint style-scope yt-formatted-string'}).get_text()
    content_url = i.find("a", attrs={"class":'yt-simple-endpoint style-scope ytd-video-renderer'})["href"]
    
    video_list.append([name, title, 'https://www.youtube.com/' + content_url])
    

## 자료 저장
# 데이터 프레임 만들기
new = pd.DataFrame(columns=['Channel', 'title' , 'url_link'])

# 자료 집어넣기
for i in range(len(video_list)):
    new.loc[i] = video_list[i]

# 저장하기
# 현재 작업폴더 안의 data 폴더에 저장
video_list_dir = "./" # 저장할 디렉토리
new.to_csv(video_list_dir+"Youtube_search_list.csv", index=False, encoding='utf-8-sig')

# 브라우저 닫기
browser.close()

new_url_list = new['url_link'].values.tolist()
new_title_list = new['title'].values.tolist()

list_for_download = []


for i, j in zip(new_title_list, new_url_list):
    list_for_download.append([i,j])

#for i in new_comment_list:
#    download_video()

for i in list_for_download:
    Comment_Crawl(i[0], i[1])