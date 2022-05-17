from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException as WDE
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from Comment_Crawl import Comment_Crawl
from download_video import download_video
from selenium.webdriver.common.by import By
from MakeNode import MakeNode
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)



url = "https://youtube.com/"

SearchDataFrame = pd.DataFrame({'Comic':["짤툰", "웃긴"],
                                                        'Action':["액션", "전투"],
                                                        'Sing': ["노래", "팝송"],
                                                        'Sad':["슬픈", "Sad"]})



keyword = input("검색: ")

finished_line = 50000

path = "D:/Capstone/chromedriver.exe"

browser = webdriver.Chrome(path, options=chrome_options)

browser.get(url)
time.sleep(2)

search = browser.find_element_by_name("search_query")
time.sleep(1)
search.send_keys(keyword)
time.sleep(1)
search.send_keys(Keys.ENTER)

present_url = browser.current_url
browser.get(present_url)

last_page_height = browser.execute_script("return document.documentElement.scrollHeight")

while True:
    print("======================= 스크롤 중 =======================")
    try:
        browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
    
        new_page_height = browser.execute_script("return document.documentElement.scrollHeight")
    
        if new_page_height > finished_line:
            break;
    
        else:
            last_page_height = new_page_height
    except:
        print("======================= Error =======================")
        continue
        
        
print("======================= 스크롤 완료 =======================")
        
html_source = browser.page_source

soup = BeautifulSoup(html_source, 'lxml')

test = soup.find_all("ytd-video-renderer", attrs={"class":'style-scope ytd-item-section-renderer'})

video_list = []

for i in test:
    try:
        title = i.find("yt-formatted-string", attrs={"class":'style-scope ytd-video-renderer'}).get_text()
        name = i.find("a", attrs={"class":'yt-simple-endpoint style-scope yt-formatted-string'}).get_text()
        content_url = i.find("a", attrs={"class":'yt-simple-endpoint style-scope ytd-video-renderer'})["href"]
    
        video_list.append([name, title, 'https://www.youtube.com/' + content_url])
    except:
        print("======================= Error =======================")
        continue
    

## 자료 저장
# 데이터 프레임 만들기
new = pd.DataFrame(columns=['Channel', 'title' , 'url_link'])

# 자료 집어넣기
for i in range(len(video_list)):
    
    new.loc[i] = video_list[i]

# 저장하기
# 현재 작업폴더 안의 data 폴더에 저장
video_list_dir = "./Capstone_Design/" # 저장할 디렉토리
new.to_csv(video_list_dir+"Youtube_search_list.csv", index=False, encoding='utf-8-sig')

print("======================= 파일 내보내기 완료 =======================")

# 브라우저 닫기
browser.close()

new_url_list = new['url_link'].values.tolist()
new_title_list = new['title'].values.tolist()

list_for_download = []


for i, j in zip(new_title_list, new_url_list):
    list_for_download.append([i,j])

'''for i in list_for_download:
    Comment_Crawl(i[0], i[1])'''

for i in list_for_download:
    try:
        download_video(i[1], "Comic")
    except:
        print("======================= Error =======================")
        continue
    

print("======================= 노드 만드는 중 =======================")

def Read_csv():
    df = pd.read_csv("./Capstone_Design/Youtube_search_list.csv")

    return df

data = Read_csv();

for i in range(len(data)):
    data['url_link'].loc[i] = "/Capstone_Design/Movie/" +data['title'].loc[i]+".mp4";

node = MakeNode("bolt://localhost:7687", "neo4j", "wltn1018")

for i in range(len(data)):
    title = str(data['title'].loc[i])
    url_link = str(data['url_link'].loc[i])
    print("================실행=================")
    node.Add_Contents(title, url_link);


for i in range(len(data)):
    title = str(data['title'].loc[i])
    node.Add_Relation("Comic", title)

node.close()