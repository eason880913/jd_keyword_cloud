import requests
from bs4 import BeautifulSoup
import re
import json
import os
from datatojson import * #從datatojson這個檔案import 全部funtion
from wordcloudgenerator import *
from urls_crawler import *

# Configuration
driver_path = '/Users/eason880913/Desktop/internship/daily/jd_keyword_cloud/chromedriver'
font_path = './Fonts/msjh.ttc' #path of your font size
dictionary_path = "./dictionary/dict_for_jieba.txt" #jieba補充包
stop_word_path = "./dictionary/my_stopwords.txt" #斷詞補充包
mask_path = './internship.jpeg'#輸出要長什麼樣的照片位置
num_of_pages = 10 #設定抓幾頁
project = 'data'#資料夾名稱
keyword = "數據"#找尋的關鍵字
# End of configuration 

#單純幫你建立檔案，不然檔案會很亂
def folder_maker(project):
    if not os.path.isdir('result/'+project):
        os.mkdir('result/'+project)
        print('foldmer_ma')


def main(project, num_of_pages, keyword, driver_path, dictionary_path, stop_word_path, font_path, mask_path):
    folder_maker(project)
    csv_of_urls(project, num_of_pages, keyword)
    driver = init_selenium(driver_path)
    download_content(project,driver)
    word_cloud_generator(dictionary_path=dictionary_path, stop_word_path=stop_word_path, font_path=font_path, project_name=project, mask_path=mask_path)

if __name__ == "__main__":
    main(project, num_of_pages, keyword, driver_path, dictionary_path, stop_word_path, font_path, mask_path)