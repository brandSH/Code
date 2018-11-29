# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#功能：对PCM进行分析，获得PCM中DTMF信号值，输出为由DTMF信号值、信号开始的采样点位置、信号结束的采样点位置为元素的List。
#目前仅支持16bit采样深度单声道，最好先将采样率转换到8000Hz
#主功能函数：DTMFRecognition()


#2018-3-23 V2

#---王展---
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import division
import os
import sys
import math
import time
import numpy as np
import heapq
from matplotlib import pyplot as plt  

#reload(sys)  
#sys.setdefaultencoding('utf-8') 


#获取PCM的采样值列表
#SampleRate 采样率
#PCMPath PCM文件相对地址或绝对地址
def getSampleValueList(PCMPath,SampleRate):
    SampleDepth = 16
    PCMBytes = open(PCMPath,'rb')
    getSampleValueList = []
    SampleValueL = 0
    SampleValueH = 0
    #print os.path.getsize(PCMPath)
    
    for i in range(os.path.getsize(PCMPath)//2):
        SampleValueL = ord(PCMBytes.read(1))
        SampleValueHByte = ord(PCMBytes.read(1))
        
        if SampleValueHByte >= 128: #是否为负数
            SampleValueH = SampleValueHByte * 256
            getSampleValueList.append(int(SampleValueL+SampleValueH-65536))
        else:   #是否为正数或0
            SampleValueH = SampleValueHByte * 256                         
            getSampleValueList.append(int(SampleValueL+SampleValueH))
    PCMBytes.close()
    return getSampleValueList  

#获取PCM中DTMF的值
#SampleValueList 采样值列表
def DTMFRecognition(SampleRate, PCMPath, SampleValueList):
    
    DTMFNum = []
    #nframes = os.path.getsize(PCMPath)//2      #16位PCM
    ALLframesCount = len(SampleValueList)
    print 'ALLframesCount = ' + str(ALLframesCount)
    #df=SampleRate/(Allnframes-1)  #频率分辨率，是指将两个相邻谱峰分开的能力

    step = SampleRate//50   #设置分析间隔，即帧长
    df=SampleRate/step      #计算分辨间隔
    FrameID = 0     #帧ID
    
    #逐帧进行DTMF识别
    for i in range(1, ALLframesCount, step):
        FrameID = FrameID + 1
        FrameStart = i
        #print 'i = ' + str(i)
        #print 'FrameID = ' + str(FrameID)
        OneFrameSampleValue = []
        #获取帧的所有采样值
        #print 'FrameID - 1 = ' + str(FrameID - 1)
        for ii in range(step * (FrameID - 1 ), i + step -1):                
            OneFrameSampleValue.append(SampleValueList[ii])                
        freq=[df*n for n in range(0,step)]  #计算每个采样频率
        #print 'len(OneFrameSampleValue) = ' + str(len(OneFrameSampleValue))
        #print str(OneFrameSampleValue)
        transformed=np.fft.fft(OneFrameSampleValue)  #进行FFT变换，输出元素为复数
        d=int(len(transformed)/2)  #计算音频的最高频率（奈奎斯特）
        while freq[d]>2000:  #去除2000Hz以上频率
            d-=10  
        freq=freq[:d]  
        transformed=transformed[:d]  
        transformed2 = []   #保存模
        for i,data in enumerate(transformed):  
            transformed[i]=abs(data)  #求复数的模，但输出还是虚部为0的复数，实部为模
            transformed2.append(int(abs(transformed[i])))    
        
        #plt.subplot(212)  
        #plt.plot(freq,transformed,'r-')    
        #plt.xlabel('Freq/Hz')  
        #plt.ylabel('Ampltitude')  
        #plt.title('freq/ampltitude')         
        #plt.show()
        
        temp = map(transformed2.index, heapq.nlargest(len(transformed2),transformed2))  #通过堆来获取从大到小的索引
    
        max_freq = 0
        min_freq = 0
        
        #根据模对应的频率找出DTMF高频
        for i in range(len(temp)):
            #print 'Hi = ' + str(i)
            if 1100 < freq[temp[i]] < 1750:
                max_freq = freq[temp[i]]
                break
        
        #根据模对应的频率找出DTMF低频
        for i in range(len(temp)):
            #print 'Li = ' + str(i)
            if 600 < freq[temp[i]] < 1010:
                min_freq = freq[temp[i]]
                break    

        #判断是否可能为DTMF信号
        if max_freq == 0 or min_freq == 0:
            print str(FrameID) + ' frame is not DTMF signal!'
        else:         
            #print 'DTMF freq ',max_freq,min_freq  
            DTMHzHigh = [1209, 1336, 1477, 1633]
            DTMHzLow = [697, 770, 852, 941]
            
            NumberHighID = 5   #赋初值，防止出现0错误，之所以为5是为了大于DTMF矩阵（4 x 4）的行列长
            NumberLowID = 5    #赋初值，防止出现0错误
            #将相邻高频的间隔的一半作为安全区，获取高频的位置
            for i in range(len(DTMHzHigh)):
                if abs(max_freq - DTMHzHigh[i]) < 60:
                    NumberHighID = i
                    #print 'NumberHighID: ' + str(NumberHighID)
                    
            #将相邻低频的间隔的一半作为安全区，获取低频的位置
            for ii in range(len(DTMHzLow)):
                if abs(min_freq - DTMHzLow[ii]) < 35:
                    NumberLowID = ii
                    #print 'NumberLowID: ' + str(NumberLowID)
            
            #通过进一步筛选出DTMF可能性高的帧进行DTMF识别
            if NumberHighID == 5 or NumberLowID == 5:   #等于5表示没有频率符合要求
                print str(FrameID) + ' frame is not DTMF signal!'
            else:   
                DTMFNumber = [(1,2,3,'A'), (4,5,6,'B'), (7,8,9,'C'), ('*',0,'#','D')]                
                Number = DTMFNumber[NumberLowID][NumberHighID]
                DTMFNum.append((Number, FrameStart))
                #print 'Number is ' + str(Number)
        
    
    #获取DTMF信号所对应的还是样本ID和样本数
    DuplicateCount = 0
    RealNumber = []
    DTMFStart = 0
    for i in range(1, len(DTMFNum)):
        #print DTMFNum[i]
        if DTMFNum[i][0] == DTMFNum[i-1][0]:
            if DTMFStart == 0 :
                DTMFStartID = DTMFNum[i-1][1]
                DTMFStart = 1
            DuplicateCount = DuplicateCount + 1
            #防止漏最后一个数值
            if i == len(DTMFNum) - 1 and DuplicateCount >= 3 :
                RealNumber.append((DTMFNum[i][0], DTMFStartID, DTMFStartID + step*DuplicateCount))
                DuplicateCount = 0                
        else:
            if DuplicateCount >= 3 :
                RealNumber.append((DTMFNum[i-1][0], DTMFStartID, DTMFStartID + step*DuplicateCount))
                DuplicateCount = 0
                DTMFStart = 0
            else:
                DuplicateCount = 0
                DTMFStart = 0
        
    return RealNumber

#调试
if __name__ == "__main__": 
    SampleRate = 8000
    PCMPath = 'C4.pcm'
    SampleValueList = getSampleValueList(PCMPath, SampleRate)
    Number = DTMFRecognition(SampleRate, PCMPath, SampleValueList)
    print 'Number List: ' + str(Number)
    for i in range(len(Number)):
        print str(Number[i][0]) + ' start at ' + str(Number[i][1] / 8000) + 's.'
   
    