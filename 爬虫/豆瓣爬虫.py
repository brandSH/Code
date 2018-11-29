#-*- coding: utf-8 -*-
import urllib2
import base64
from bs4 import BeautifulSoup as bs
import re
import chardet
import sys  
import jieba
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
import pylab 
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)

#print sys.getdefaultencoding() 
#设置默认编码格式为utf-8
reload(sys)  
sys.setdefaultencoding('utf-8') 

def GetNowPlayingid(URL,TopNo):
    response = urllib2.urlopen(URL)
    responseStr = response.read().decode('utf-8') 
    #print responseStr
    
    soup = bs(responseStr,'html.parser')
    nowplaying_movie = soup.find_all('div', id='nowplaying')
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
    #print nowplaying_movie_list[0]
    
    nowplaying_list = [] 
    for item in nowplaying_movie_list:        
        nowplaying_dict = {}        
        nowplaying_dict['id'] = item['data-subject']       
        for tag_img_item in item.find_all('img'):            
            nowplaying_dict['name'] = tag_img_item['alt']            
            nowplaying_list.append(nowplaying_dict)
    print nowplaying_list[TopNo]['id']  
    return nowplaying_list[TopNo]['id']

def GetComments(URL):
    requrl = URL
    resp = urllib2.urlopen(requrl) 
    html_data = resp.read().decode('utf-8') 
    soup = bs(html_data, 'html.parser') 
    comment_div_lits = soup.find_all('div', class_='comment')
    eachCommentList = []
    for item in comment_div_lits: 
        if item.find_all('p')[0].string is not None:     
            eachCommentList.append(item.find_all('p')[0].string)
    comments = ''
    for k in range(len(eachCommentList)):
        comments = comments + eachCommentList[k].strip()
    print comments
    return comments

def GetWordCloud(comments):
    cleaned_comments = re.sub('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、：~@#￥%……&*（）]+'.decode('utf8'),''.decode('utf8'),comments.decode('utf8'))
    print cleaned_comments
    
    segment = jieba.lcut(cleaned_comments)
    words_df=pd.DataFrame({'segment':segment})
    print words_df.head()
    
    stopwords=pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='utf-8')#quoting=3全不引用
    words_df=words_df[~words_df.segment.isin(stopwords.stopword)]
    print words_df.head()
    
    words_stat=words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
    words_stat=words_stat.reset_index().sort_values(by=["计数"],ascending=False)
    print words_stat.head()
    
    wordcloud=WordCloud(font_path="simhei.ttf",background_color="white",max_font_size=80) #指定字体类型、字体大小和字体颜色
    word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
    word_frequence_list = []
    for key in word_frequence:
        temp = (key,word_frequence[key])
        word_frequence_list.append(temp)
     
    wordcloud=wordcloud.fit_words(dict(word_frequence_list))
    plt.imshow(wordcloud)
    plt.show()
    plt.savefig("result.jpg")    

#调试
if __name__ == "__main__":  
    MovieTopOneid = GetNowPlayingid('http://movie.douban.com/nowplaying/shanghai/',0)
    #comments = GetComments('http://movie.douban.com/subject/' + MovieTopOneid + '/comments' +'?' +'start=0' + '&limit=20' )
    comments = ''
    for i in range(2):        
        print 'i=' + str(i)
        comments = comments + GetComments('http://movie.douban.com/subject/' + MovieTopOneid + '/comments' +'?' +'start=' + str(i*20) + '&limit=20' )
        print 'comments=' + comments
    GetWordCloud(comments)