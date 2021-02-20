from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
import time
import json
import os
import csv 

# project = 'Process_engineer'

def init_selenium(driver_path):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument('--max_old_space_size')    
    chrome_options.add_experimental_option("prefs",prefs) # turn of notification window\
    driver = webdriver.Chrome(driver_path,chrome_options=chrome_options)
    return driver

def download_content(project,driver):
    with open(f'./{project}/{project}.csv', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        # 以迴圈輸出每一列
        for row in rows:
            # print(row[0])
            url = row[0]
            try:
                driver.get(url)
                res = driver.page_source
                soup = BeautifulSoup(res,'lxml')
                content = soup.select('[class="mb-5 r3 job-description__content text-break"]')[0].text
                with open (f'{project}/{project}.txt','a',encoding='utf-8') as f:
                    f.write(content)
            except:
                print(row[0])
        driver.quit()

# Execution
# driver = init_selenium()
# download_content(project,driver)