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
import matplotlib.pyplot as plt  #若路径中有中文则import会报错，或者用下面方法解决：
####################
#改_init_.py文件，

## 与源文件的代码区别在于第一行与最后一行的字符串前添加了标记 b 
#_backend_loading_tb = b"".join(
    #line for line in traceback.format_stack()
    ## Filter out line noise from importlib line.
    #if not line.startswith(b'  File "<frozen importlib._bootstrap'))

####################
import matplotlib
from wordcloud import WordCloud
import pylab 
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)

#print sys.getdefaultencoding() 
#设置默认编码格式为utf-8
reload(sys)  
sys.setdefaultencoding('utf-8') 




def GetWordCloud(Words):
    cleaned_Words = re.sub('[\s+\!\/_,$%^*(+\"\']+|[+——！，。？、：~@#￥%……&*（）\n]+'.decode('utf8'),''.decode('utf8'),Words.decode('utf8'))
    print cleaned_Words
    
    segment = jieba.lcut(cleaned_Words)
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
    wordcloud.to_file('yuntu.png')
    plt.imshow(wordcloud)
    plt.show()

#调试
if __name__ == "__main__":  
    f = open('2018.txt')
    Words = ''.join(f.readlines())  #list转字符串
    GetWordCloud(Words)
    f.close()