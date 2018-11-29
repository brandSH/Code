# -*- coding: utf-8-*-
# owner: cuiyifei wangyichao

import os
import subprocess
from aip import AipOcr
import json 
import types
import math
import time
import datetime
import subprocess
import os
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#获取纯码流文件名
def file_paths(path):
    dirs = os.listdir(path)
    return dirs


#百度图片识别模块 获取json类型里识别的数据 计算延时，图片格式选用jpg可提高识别率

def picturedelay(VidioToBmp,dir_1,i):
    #""" 你的APPID AK SK """
    if 0<= i <500:
        APP_ID = '11181750'
        API_KEY = 'ozSsdaiAi1ahOi0jIUa8T0ZG'
        SECRET_KEY = 'ex8dlMtriN1QGLPgmw0OqzAN3qQxogzV' 
    elif 500<= i <1000 :
    
        APP_ID = '11181692'
        API_KEY = 'GHYCfWunZAPKjn2tjy2h4BTA'
        SECRET_KEY = 'SHEvNaILZGMRD5erZczjyvYvew5dCynf'   
        
    elif 1000<= i <1500 :
        APP_ID = '10626237'
        API_KEY = 'us6qEBGEokbS6po9mrz9GPdv'
        SECRET_KEY = 'AadChookpxZYMYcC7lOsBWGaFLAoLhkz'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    #上传文件
    filePath = VidioToBmp
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    #参数
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    #获取result
    result=client.basicAccurate(get_file_content(filePath) , options)
    print result
    if result['words_result_num'] == 1:
        strtime = result['words_result'][0]['words']
        #print strtime
    if result['words_result_num'] > 1:
        try:
            strtime= ''
            for i in range(0,result['words_result_num']):
                #print result['words_result'][i]['words']
                strtime += str(result['words_result'][i]['words'])
                #print strtime
        except:
            pass

    #if result['words_result_num'] >2:
        #strtime= ''
        #for i in [0,(result['words_result_num'])-1]:
            ##print result['words_result'][i]['words']
            #strtime += str(result['words_result'][i]['words'])
            ##print strtime
    try:
        if 'O'in strtime:
            strtime = strtime.replace('O','0')
        if 'I'in strtime:
            strtime = strtime.replace('O','0')
        def OnlyCharNum(s,oth=''):
            s2 = s.lower();
            fomart = '0123456789'
            for c in s2:
                if not c in fomart:
                    s = s.replace(c,'');
            return s
        #print OnlyCharNum(strtime)
        l = len(OnlyCharNum(strtime))
        str1 = OnlyCharNum(strtime)[0:l/2][-5:]
        print str1
        str2 = OnlyCharNum(strtime)[l/2:l][-5:]
        print str2
        delay= int(str2) - int(str1)
        #print delay
        time1= dir_1
        #print time1
        print "Time: %s delay:%sms\r\n"%(time1,delay)
        if 0<delay<10000:

            f= open("vedio_delay.txt",'a')
            f.write("Time: %s delay:%sms\r\n"%(time1,delay))
            f.close()
        else:
            delay = 0
            f= open("vedio_delay.txt",'a')
            f.write("Time: %s delay:%sms\r\n"%(time1,delay))
            f.close()            
    except:
        pass

#写视频延时到文件
def WriteDelay(VideoDelay):
    with open("video_delay_result.txt", "a+") as f:
        src = "%s ms\n" % VideoDelay
        f.write(src.encode())
        f.close()  
        
      
path =  os.getcwd()
dirs = file_paths(path)
print dirs
i = 0 
for dir_1 in dirs:
    time.sleep(5)
    VidioToBmp = path+'\\'+dir_1+'\\'+'videotobmp.jpg'
    try:
        picturedelay(VidioToBmp,dir_1,i)
        print VidioToBmp
    except:
        pass 
    i = i+1