# -*- coding: utf-8 -*-
"""
Created on Sat July 18 15:00:00 2020

The program first reads a json file full of comment, conduct word segmentation, and finally plot word cloud
Must have: 1. Fonts folder 2. dictionary folder

@author: Eason
"""
import os, errno
import json
import jieba
import jieba.analyse
import re
import random
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import jieba.posseg as pseg

# scriptpath = os.path.dirname(os.path.abspath('__file__'))
# # print("Script path is at: " + scriptpath)
# os.chdir(scriptpath)

# Configuration
# font_path = 'Fonts/msjh.ttc' # specify the full path of your font size
# dictionary_path = "/Users/eason880913/Desktop/internship/daily/jd_keyword/dictionary/dict_for_jieba.txt"
# stop_word_path = "/Users/eason880913/Desktop/internship/daily/jd_keyword/dictionary/my_stopwords.txt"
# project = 'financial'
# End of configuration 

# function family

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

def movestopwords(sentence,filepath):
    stopwords = stopwordslist(filepath)  
    outstr = ''
    for word in sentence:
        if word not in stopwords:
            if word != '\t'and'\n':
                outstr += word
                # outstr += " "
    return outstr

def get_comment_content(json_file):
    words_collector = ''
    for k,v in json_file.items():
        for k2,v2 in v['comment'].items():
            if len(v2['comment']) > 0:
                words_collector += v2['comment'] +'\n'
            else:
                continue
    return(words_collector)
    
    
def get_post_content(json_file):
    words_collector = ''
    for k,v in json_file.items():
        if len(v['article_text']) > 0:
            words_collector += v['article_text'] +' '
        else:
            continue
        #print(v['article_text'])
    return(words_collector)
    


def green_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    '''
    function to alter word color in a wordcloud
    
    e.g.,
    plt.imshow(wordcloud.recolor(color_func=green_color_func, random_state=3),interpolation='bilinear',cmap=plt.cm.gray)
    
    '''
    return "hsl(100, %d%%, %d%%)" % (random.randint(60, 100) , random.randint(0, 60))

def mix_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(%d, %d%%, %d%%)" % (random.randint(0, 100) , random.randint(60, 100) , random.randint(0, 60))

def bluish_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(200, %d%%, %d%%)" % ( random.randint(100, 180) , random.randint(100, 180))



def make_wordcloud(data, font_path, project_name, mask = None, title = None):
    '''
    the wrapper of generating word cloud
    
    '''
    stopwords = set(STOPWORDS)
    add_stopword = ['https','http']
    [stopwords.add(i) for i in add_stopword]
    
    if mask is None:
        wordcloud = WordCloud(
        background_color='white',
        font_path=font_path,
        max_words=400,
        max_font_size=60, 
        margin=2,
        scale=3,
        mode="RGBA",
        stopwords=stopwords,
        #contour_width=3,
        #contour_color='blue',
        random_state=1 # chosen at random by flipping a coin; it was heads
        ).generate(str(data))
    else:
        wordcloud = WordCloud(
        background_color='white',
        font_path=font_path,
        max_words=140,
        max_font_size=200, 
        margin=2,
        scale=3,
        mask=mask,
        mode="RGBA",
        stopwords=stopwords,
#        width=800,
#        height=400,
#        contour_width=3,
#        contour_color='blue',
        random_state=1 # chosen at random by flipping a coin; it was heads
        ).generate(str(data))

    fig = plt.figure(1, figsize=(50, 50))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    # recolor section
#    image_colors = ImageColorGenerator(mask)
#    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
#    plt.imshow(wordcloud.recolor(color_func=bluish_color_func, random_state=3),interpolation='bilinear',cmap=plt.cm.gray)
    
#    plt.imshow(wordcloud,interpolation='bilinear',cmap=plt.cm.gray)
#    plt.savefig("img/{}.png".format(project_name), format="png")
#    plt.show() # uncomment it to see the result in the terminal

    # change here for specific folder
    wordcloud.to_file("{}.png".format(project_name))

# End of functions




    
def word_cloud_generator(dictionary_path, stop_word_path, font_path, project_name, mask_path):
    '''
    wrapper of word cloud generation process
    
    parameters:
    -----------
    dictionary_path = dictionary for jieba
    font_path = font for plotting a word cloud
    project_name = name of a project (defined by user) 
    
    '''
    '''output_folder = 'img'
    try:
        os.makedirs(output_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise'''
    
    with open(f"{project_name}/{project_name}.txt",encoding='utf-8') as f:  
        content = f.read()

    jieba.load_userdict(dictionary_path) # load dictionary       
      
    # [1] make the word cloud over post content first
    print('Generating the WordCloud ...')
    # preprocessing
    words_collector = re.sub(pattern='http\S+\s?',repl="",string=content)
    jieba.enable_paddle()
    words = pseg.cut(words_collector,use_paddle=True) #paddle模式

    words_collector = ''
    # 斷詞完會有 詞跟詞性 我這裡設定只把名詞抓下來 
    for word, flag in words:
        if flag == 'n':
            # print('%s %s' % (word, flag))
            words_collector += word+'\n'

    # make sure that words_collector is not empty
    if len(words_collector)>0:
        
        # word segmentation
        seg_list = jieba.cut(words_collector, cut_all=False) 
        seg_list = " ".join(seg_list)
        
        # remove stop word
        listcontent = movestopwords(seg_list, stop_word_path) 
        listcontent = re.sub(pattern='\\s+|\\n',repl=' ',string=listcontent)

        # load the image mask              
        like_mask = np.array(Image.open(mask_path))
        
        # output the word cloud
        make_wordcloud(listcontent,font_path,mask=like_mask,project_name=f'{project_name}/{project_name}_post_WordCloud')
    else:
        print('no vocab in words_collector. skipping through')
    
    
    print('WordCloud generation completed!')
         


# Execution
# word_cloud_generator(dictionary_path=dictionary_path, font_path=font_path, project_name=project)







# Do not touch anything bellow !!!
'''
plotting wordcloud based on weights of words
'''
#jieba.analyse.set_stop_words(stop_word_path)

#keywords = jieba.analyse.textrank(words_collector, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v','nsf','nt','nz','nl','ng','a','ad'))
#for item in keywords:
#    print (item[0], item[1])


