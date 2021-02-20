import requests
from bs4 import BeautifulSoup
import re
import json
import os
from datatojson import * #從datatojson這個檔案import 全部funtion
from wordcloudgenerator import *

# Configuration
driver_path = './chromedriver'
font_path = './Fonts/msjh.ttc' #path of your font size
dictionary_path = "./dictionary/dict_for_jieba.txt" #jieba補充包
stop_word_path = "./dictionary/my_stopwords.txt" #斷詞補充包
mask_path = './internship.jpeg'#輸出要長什麼樣的照片位置
num_of_pages = 2 #設定抓幾頁
project = 'ml'#資料夾名稱
keyword = "機器學習"#找尋的關鍵字


# End of configuration 

#單純幫你建立檔案，不然檔案會很亂
def foldmer_maker(project):
    if not os.path.isdir(project):
        os.mkdir(project)

#爬urls的funtion
def csv_of_urls(project):
    # 設定 header & cookies 是因為有些網頁有防爬蟲
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    cookies={"Cookie":"JSESSIONID=137FDD5DAE17F532FE862C4343C66110; JSESSIONID=A735FCEAD2A8DC9174288C3864ED2601"}

    for i in range(1,num_of_pages):#設定要抓幾頁抓幾頁
        url = f'https://www.104.com.tw/jobs/search/?ro=1&kwop=7&keyword={keyword}&order=12&asc=0&page={i}&mode=s&jobsource=2018indexpoc'
        res = requests.get(url,headers=headers,cookies=cookies)
        soup = BeautifulSoup(res.content,'lxml')
        articles = soup.select('[class="b-tit"] a')

        num_of_article = int(len(articles))
        
        #超出資料量停止
        if num_of_article == 0:
            break
        
        #打每個url存入csv
        for j in range(num_of_article):
            urls = soup.select('[class="b-tit"] a')[j]['href']
            with open(f"{project}/{project}.csv",'a') as f:
                f.write('https:'+urls+'\n')

if __name__ == "__main__":
    foldmer_maker(project)
    csv_of_urls(project)
    driver = init_selenium(driver_path)
    download_content(project,driver)
    word_cloud_generator(dictionary_path=dictionary_path, stop_word_path=stop_word_path, font_path=font_path, project_name=project, mask_path=mask_path)