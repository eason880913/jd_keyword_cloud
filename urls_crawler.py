import requests
from bs4 import BeautifulSoup
import re
import json
import os
from datatojson import * #從datatojson這個檔案import 全部funtion
from wordcloudgenerator import *

# Configuration
# driver_path = './chromedriver'
# num_of_pages = 2 #設定抓幾頁
# project = 'ml'#資料夾名稱
# keyword = "機器學習"#找尋的關鍵字
# End of configuration 

#爬urls的funtion
def csv_of_urls(project, num_of_pages, keyword):
    # 設定 header & cookies 是因為有些網頁有防爬蟲
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    cookies={"Cookie":"JSESSIONID=137FDD5DAE17F532FE862C4343C66110; JSESSIONID=A735FCEAD2A8DC9174288C3864ED2601"}
    print("save urls in csv...")
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
        try:
            os.remove(f"result/{project}/{project}.csv")
        except:
            raise
        
        for j in range(num_of_article):
            urls = soup.select('[class="b-tit"] a')[j]['href']
            with open(f"result/{project}/{project}.csv",'a') as f:
                f.write('https:'+urls+'\n')

# Execution
# csv_of_urls(project)