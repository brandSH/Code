#-*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#主功能函数：VoiceRecognition()

#-----2017-8-29-----
#调用百度语音Web API进行语音识别
#主功能函数：VoiceRecognition(WAVFileName)
#测试时需要连接Internet！！

#-----2017-8-29-----
#添加网络超时错误捕获处理

#-----2017-8-29-----
#将语音识别结果字符串转为字典处理

#-----2017-9-11-----
#使用正则表达式计算中文字个数

#---王展---
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
#from __future__ import unicode_literals
from __future__ import division     #设置脚本所有除法默认是精确除，必须放第一行
import wave  
import urllib, urllib2, pycurl  
import base64  
import json  
import StringIO     #用于在内存缓冲区中读写数据
import re
import chardet
import sys

#创建百度语音识别token
def get_token():  
    apiKey = "j0rfqnbvCGhAYA62u7sjGq8w"  
    secretKey = "889490f7ae3a885dd144071b5d235720"  
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;  
    res = urllib2.urlopen(auth_url)  
    json_data = res.read()  
    return json.loads(json_data)['access_token']      

#将WAV上传至百度语音识别服务器并获取返回的结果 
#WAV文件必须是8KHz、16Bit、单声道
#获取语音识别后的句子和文字个数（不包含标点、特殊字符、数字、英文字母）
def VoiceRecognition(WAVFileName):  
    #fp = wave.open(WAVFileName.decode('utf-8').encode('gbk'), 'rb') 
    try:
        fp = wave.open(WAVFileName, 'rb')
        nf = fp.getnframes()  
        f_len = nf * 2  
        audio_data = fp.readframes(nf)  
        token = get_token() 
        srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + 'D4BED9BDFBB9' + '&token=' + token     #cuid为测试PC的MAC地址，可以不修改
        http_header = [  
            'Content-Type: audio/pcm; rate=8000',  
            'Content-Length: %d' % f_len  
        ]  
        ServerResponse = StringIO.StringIO() 
    
        c = pycurl.Curl()  
        c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode  
        #c.setopt(c.RETURNTRANSFER, 1)  
        c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict  
        c.setopt(c.POST, 1)  
        c.setopt(c.CONNECTTIMEOUT, 30)      #设置链接超时时间
        c.setopt(c.TIMEOUT, 30)     #设置下载超时时间
        #c.setopt(c.WRITEFUNCTION, dump_res)
        c.setopt(c.WRITEFUNCTION, ServerResponse.write)     #写回调，将返回值写入ServerResponse
        c.setopt(c.POSTFIELDS, audio_data)      #设置psot过去的数据，注意是一个字典样式的字符串
        c.setopt(c.POSTFIELDSIZE, f_len)      
        c.perform()     #执行curl命令，pycurl.perform()没有返回值
    except Exception, e:
        ResultStr = str(e)
        ResultStrLen = 0
        return (ResultStr,ResultStrLen)
    ServerResponseStr = ServerResponse.getvalue()
    ServerResponse.close()
    ServerResponseDic = eval(ServerResponseStr)     #字符串转字典
    ErrMsg = ServerResponseDic['err_msg']
    if ErrMsg == 'success.':
        #print ServerResponseDic['result'][0].decode('utf-8').encode('gbk')
        ResultStr = ServerResponseDic['result'][0].strip('\n')    #strip('\n')去除换行符
        #使用这则表达式进行字符串替换时一定把所有字符转decode成utf-8
        ResultStrWithOutPunctuation = re.sub('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、：~@#￥%……&*（）\w]+'.decode('utf8'),''.decode('utf8'),ResultStr.decode('utf8')) 
        ResultStrLen = len(ResultStrWithOutPunctuation)         #不含标点符号、特殊字符、数字、英文  
        return (ResultStr,ResultStrLen)
    else:
        ResultStr = 'Recognition Failed! ' + ServerResponseStr.strip('\n')
        ResultStrLen = 0
        return (ResultStr,ResultStrLen)

#调试
if __name__ == "__main__":  
    WAVFileName = 'FB_male_female_double-talk_seq_L.wav'
    #PCMAC = 'D4BED9BDFBB9'
    (ResultStr,ResultStrLen) = VoiceRecognition(WAVFileName)
    print ResultStr
    print ResultStrLen