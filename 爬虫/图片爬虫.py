# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import requests as rq
import re
import os


def fetch_pictures(url):
    html_content = rq.get(url).text
    r = re.compile(r'"objURL":"(.*?)"')
    picture_url_list = r.findall(html_content.decode('utf-8'))
    os.chdir(u'D:\\wyc\\ai_sucai')
    os.mkdir(word)
    os.chdir(os.path.join(os.getcwd(), word))
    for i in range(len(picture_url_list)):
        picture_name = str(i) + '.jpg'
        try:
            urllib.urlretrieve(picture_url_list[i], picture_name)
            print("Success to download " + picture_url_list[i])
        except:
            print("Fail to download " + picture_url_list[i])
if __name__ == '__main__':
    key_words = [u'猫脸',u'狗脸',u'白种男人脸',u'白种女人脸']
    for word in key_words:
        fetch_pictures("https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1528210492714_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word="+word)