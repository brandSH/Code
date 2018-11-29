# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#主功能函数：AECResultAutoAnalysis()

#目前仅支持16bit采样深度单声道
#该版本新增了对AEC单讲回声失效时的结果通过统计回声的数量、长度、音量进行了量化
#测试结果按AEC模式分为两个文件：SingleTalk.csv    DoubleTalk.csv
#SingleTalk.csv字段：TestTime,Result,Cooked,PeakdB,CookedTime,RefTime,Cooked/RefTime*100%,MaxVPTime,MaxVPTimedB,MiniVPTime,MiniVPTimedB,MaxVPdB,MaxVPdBTime,MiniVPdB,MiniVPdBTime,AVGVPTime,AVGVPdB,VPCount
#DoubleTalk.csv字段：TestTime,Result,Cooked,PeakdB,CookedTime,RefTime,Cooked/RefTime*100%
#VP: VoicePiece  

#-----2017-8-29-----
#增加语音识别功能，但测试时需要连接Internet！！！
#需将脚本VoiceRecognition放到相同目录下
#修改AECResultAutoAnalysis()接口为：AECResultAutoAnalysis(PCMPath,SampleRate,MinidB,RefTime,RefPeakdB,RefVLen,AECMod)
#双讲的判断条件调整为AEC后可识别文字个数
#调整.csv字段（增加语音识别结果、Cook文字个数、Ref文字个数）：
#SingleTalk.csv字段：TestTime,Result,Cooked,PeakdB,CookedTime,RefTime,Cooked/RefTime*100%,MaxVPTime,MaxVPTimedB,MiniVPTime,MiniVPTimedB,MaxVPdB,MaxVPdBTime,MiniVPdB,MiniVPdBTime,AVGVPTime,AVGVPdB,VPCount,VRRestult,CookVLen,RefVLen
#DoubleTalk.csv字段：TestTime,Result,Cooked,PeakdB,CookedTime,RefTime,Cooked/RefTime*100%,VRRestult,CookVLen,RefVLen

#---王展---
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import division
import os
import math
import time
import multiprocessing
import VoiceRecognition
import GetVoiceList
import getpass,datetime
import subprocess
import string
from sys import argv
import csv
import re
import codecs
import wave
import numpy as np 
import shutil
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#获取PCM的dB列表
def getdBList(PCMPath,SampleRate):
    SampleDepth = 16
    PCMBytes = open(PCMPath,'rb')
    dBList = []
    SampleValueL = 0
    SampleValueH = 0
    #print os.path.getsize(PCMPath)
    
    for i in range(os.path.getsize(PCMPath)//2):
        SampleValueL = ord(PCMBytes.read(1))
        SampleValueHByte = ord(PCMBytes.read(1))
        
        if SampleValueHByte >= 128: #是否为负数
            SampleValueH = SampleValueHByte * 256
            dBList.append(int(20*math.log10(abs(SampleValueL+SampleValueH-65536)/32767)))
        else:   #是否为正数或0
            SampleValueH = SampleValueHByte * 256
            if SampleValueL + SampleValueH == 0:
                dBList.append(-1000)       #使用-1000表示声音无限小
            else:                
                dBList.append(int(20*math.log10((SampleValueL+SampleValueH)/32767)))
    PCMBytes.close()
    return dBList  

#获取PCM大于MinidB的时长、最大dB值、平均dB值
def PCMGreaterThanMinidBTime(PCMdBList,SampleRate,MinidB):
    GreaterThanMinidBCount = 0
    PeakdB = PCMdBList[0]
    dBSum = 0
    GreaterThanMinidBCountList = []
    for i in range(len(PCMdBList)):
        if PCMdBList[i] > MinidB:
            GreaterThanMinidBCount = GreaterThanMinidBCount +1
            dBSum = dBSum + PCMdBList[i]
        else:
            if GreaterThanMinidBCount != 0 :
                GreaterThanMinidBCountList.append(GreaterThanMinidBCount)
                GreaterThanMinidBCount = 0    
    PeakdB = max(PCMdBList)
    AllGreaterThanMinidBTime = 0
    AllGreaterThanMinidBCount = 0
    AVGdB = 0
    for i in range(len(GreaterThanMinidBCountList)):
        AllGreaterThanMinidBTime = AllGreaterThanMinidBTime + (GreaterThanMinidBCountList[i] / SampleRate) * 1000
        AllGreaterThanMinidBCount = AllGreaterThanMinidBCount + GreaterThanMinidBCountList[i]
    if AllGreaterThanMinidBCount != 0 :        
        AVGdB = dBSum / AllGreaterThanMinidBCount
    else:
        AVGdB = -1000
    return (int(AllGreaterThanMinidBTime),PeakdB,int(AVGdB))       

#考虑到双讲AEC后的声音音量可能发生改变，因此MinidB需要做调整
def DoubleTalkPCMGreaterThanMinidBTime(PCMdBList,SampleRate,MinidB,RefPeakdB):
    PeakdB = max(PCMdBList)
    MinidB = MinidB - (RefPeakdB - PeakdB)
    (AllGreaterThanMinidBTime,PeakdB,AVGdB) = PCMGreaterThanMinidBTime(PCMdBList, SampleRate, MinidB)
    return (AllGreaterThanMinidBTime,PeakdB,AVGdB)   

#写结果
def WriteTestResult(TestResultFileName,ResultHead,Result):    
    if os.path.exists(TestResultFileName) == False:
        TestResultFile = open(TestResultFileName,'w')
        TestResultFile.write(ResultHead+'\n'+Result)
    else: 
        TestResultFile = open(TestResultFileName,'a')
        TestResultFile.write('\n'+Result)                 
    TestResultFile.close()    

def dBCompare(dBValua):
    if dBValua >= -20:
        dBScorce=0.0
    elif -20 > dBValua >= -35:
        dBScorce=0.5
    elif -35 > dBValua >= -45:
        dBScorce=0.7
    else:
        dBScorce=1.0
    return dBScorce

#AEC结果自动预判
#RefVPTime 参考测试大于MinidB的有效声音时间
#RefTime 参考序列大于MinidB的所有样本点的时间
#RefVLen 参考序列中文字的个数
#PCMPath不能还有空格
def AECResultAutoAnalysis(PCMPath,SampleRate,MinidB,RefVPTime,RefTime,RefPeakdB,RefVLen,AECMod):
    start = time.time()       
    TestTime = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    FFMPEG=multiprocessing.Process(target=os.system,args=(r'ffmpeg.exe  -f s16le -ar '+str(SampleRate)+' -ac 1 -i '+PCMPath+' -acodec pcm_s16le -ar 8000 -ac 1 out.wav -y',))
    FFMPEG.daemon=True
    FFMPEG.start()  
    FFMPEG.join()
    (VRRestult, VPAllStrLen) = VoiceRecognition.VoiceRecognition('out.wav')
    #VRRestult=VRRestult.encode('gbk')
    #print type(VRRestult)
    PCMdBList = getdBList(PCMPath, SampleRate)
    #单讲
    if AECMod == 's' or AECMod =='S':
        (AllGreaterThanMinidBTime,PeakdB,AVGdB) = PCMGreaterThanMinidBTime(PCMdBList,SampleRate,MinidB)
        AECFailPercent = (AllGreaterThanMinidBTime / RefTime) * 100
        (VoicePieceList,VoiceRefVPTimePeakdB) = GetVoiceList.GetVoiceList(PCMdBList, SampleRate, MinidB)
        VoicePieceCount = len(VoicePieceList)
        CookedVPtime = VoiceRefVPTimePeakdB[0]
        AECVPTimePercent = (CookedVPtime/RefVPTime) * 100
        TestResultFileName = 'SingleTalk.csv' 
        ResultHead = 'TestTime,Result,Cooked,PeakdB,CookedVPtime,RefVPTime,CookedTime/RefTime*100%,VPList,CookedTime,RefTime,CookedTime/RefTime*100%,MaxVPTime,MaxVPTimedB,MiniVPTime,MiniVPTimedB,MaxVPdB,MaxVPdBTime,MiniVPdB,MiniVPdBTime,AVGVPTime,AVGVPdB,VPCount,VRRestult,CookVLen,RefVLen,Scorce,average'
        VoicePieceList.sort(key = lambda x:x[1]) #
        #print VoicePieceList
        MaxVPTime = VoicePieceList[VoicePieceCount-1][1]   #VP: VoicePiece   获取最长时间片长度     
        #print   MaxVPTime
        MaxVPTimedB = VoicePieceList[VoicePieceCount-1][2]      #最长时间片的最大dB
        VoicePieceList.sort(key = lambda x:(x[1],-x[2]))    #按照元组的第一个（片时间）从小到大排序,如果第一个相同,则按照元组第2个（片最大dB）从大到小排序，从而可以得到时间最小但声音最大的片
        MiniVPTime = VoicePieceList[0][1]   #最短时间片长度
        MiniVPTimedB = VoicePieceList[0][2]     #最短时间片的最大dB
        VoicePieceList.sort(key = lambda x:x[2])    #按dB从小到大排序，若dB相同，片时间按从小到大排序
        MaxVPdB = VoicePieceList[VoicePieceCount-1][2]      #最大dB
        MaxVPdBTime = VoicePieceList[VoicePieceCount-1][1]      #最大dB所在时间片的长度
        VoicePieceList.sort(key = lambda x:(x[2],-x[0]))    #按照元组的第2个（片最大dB）从小到大排序,如果第2个相同,则按照元组第1个（片时间）从大到小排序，从而可以得到声音最小但时间最长的片
        MiniVPdB = VoicePieceList[0][2]     #最小dB
        MiniVPdBTime = VoicePieceList[0][1]     #最小dB所在时间片的长度
        AVGVPTime = (VoiceRefVPTimePeakdB[0]) // VoicePieceCount
        AVGVPdB = (VoiceRefVPTimePeakdB[1]) // VoicePieceCount
        MaxVPTimedB = VoiceRefVPTimePeakdB[2]
        VoicePieceList=str(VoicePieceList).replace(',','') 
        if CookedVPtime > 50 or MaxVPdB > -35:
            #计算单讲平均值
            #Scorce1：语音片段残留时间
            Scorce1 = ('%.2f' %(1-CookedVPtime/RefVPTime))
            #Scorce2：平均语音片段长度
            Scorce2 = ('%.2f' %(1-AVGVPTime/RefVPTime))
            #Scorce2 = ('%.2f' %(1-VoicePieceCount/12))
            #Scorce3:峰值分贝比值 划分区段
            Scorce3 = dBCompare(MaxVPdB)
            #Scorce41：最大片段残留时间/语音片段残留时间；Scorce42：最大片段所在的声音音量 划分区段
            Scorce41 = float(('%.2f' %(1-MaxVPTime/RefVPTime)))
            Scorce42 = float(dBCompare(MaxVPTimedB))
            Scorce4 = ('%.2f' %(math.sqrt(Scorce41*Scorce42)))
            print Scorce41, Scorce42, Scorce4
            #Scorce5 = ('%.2f' %(abs(MaxVPTimedB)/abs(MinidB)))
            #Scorce51：最大音量 划分区段；Scorce52：最大音量所在的语音残留时间 
            Scorce51 = Scorce3
            Scorce52 = float(('%.2f' %(1-MaxVPdBTime/RefVPTime)))
            Scorce5 = float(('%.2f' %(math.sqrt(Scorce51*Scorce52))))
            #语音识别字数
            Scorce6 = ('%.2f' %(1-VPAllStrLen/RefVLen))
            #加权平均值
            a = (float(Scorce1),float(Scorce2),float(Scorce3),float(Scorce4),float(Scorce5),float(Scorce6))
            average = 5*(np.average(a,weights=[8,1,5,1,1,8]))
            ScorceList = str(Scorce1)+' '+str(Scorce2)+' '+str(Scorce3)+' '+str(Scorce4)+' '+str(Scorce5)+' '+str(Scorce6)
            AECResult = 'F'    
            Result = ''.join(TestTime+','+AECResult+','+PCMPath+','+str(PeakdB)+','+str(CookedVPtime)+','+str(RefVPTime)+','+str(AECVPTimePercent)+','+VoicePieceList+','
                            +str(AllGreaterThanMinidBTime)+','+str(RefTime)+','+str(AECFailPercent)+','+str(MaxVPTime)+','+str(MaxVPTimedB)+','+str(MiniVPTime)+','
                            +str(MiniVPTimedB)+','+str(MaxVPdB)+','+str(MaxVPdBTime)+','+str(MiniVPdB)+','+str(MiniVPdBTime)+','+str(AVGVPTime)+','+str(AVGVPdB)+','
                            +str(VoicePieceCount)+','+VRRestult+','+str(VPAllStrLen)+','+str(RefVLen)+','+str(ScorceList)+','+str(average))
            WriteTestResult(TestResultFileName, ResultHead, Result)
        else: 
            AECResult = 'P'
            average = 5.00
            VoicePieceList=str(VoicePieceList).replace(',','') 
            Result = ''.join(TestTime+','+AECResult+','+PCMPath+','+str(PeakdB)+','+str(CookedVPtime)+','+str(RefVPTime)+','+str(AECVPTimePercent)+','+VoicePieceList+','
                            +str(AllGreaterThanMinidBTime)+','+str(RefTime)+','+str(AECFailPercent)+','*12+
                            VRRestult+','+str(VPAllStrLen)+','+str(RefVLen))+','*2+str(average)
            WriteTestResult(TestResultFileName, ResultHead, Result)
    #双讲
    elif AECMod == 'd' or AECMod =='D':      
        reload(sys)
        sys.setdefaultencoding('utf-8')        
        (AllGreaterThanMinidBTime,PeakdB,AVGdB) = DoubleTalkPCMGreaterThanMinidBTime(PCMdBList,SampleRate,MinidB,RefPeakdB)
        AECFailPercent = (AllGreaterThanMinidBTime / RefTime) * 100
        (VoicePieceList,VoiceRefVPTimePeakdB) = GetVoiceList.GetVoiceList(PCMdBList, SampleRate, MinidB)
        VoicePieceCount = len(VoicePieceList)
        CookedVPtime = VoiceRefVPTimePeakdB[0]
        AECVPTimePercent = (CookedVPtime/RefVPTime) * 100
        TestResultFileName = 'DoubleTalk.csv'
        ResultHead = 'TestTime,Result,Cooked,PeakdB,CookedVPtime,RefVPTime,CookedTime/RefTime*100%,VPList,CookedTime,RefTime,Cooked/RefTime*100%,VRRestult,CookVLen,RefVLen'
        #语音识别得分
        DValue = VPAllStrLen - RefVLen
        if DValue > 0:
            AECResult = 'F'  
            Scorce1 = 0.0   
            Scorce2 = float((CookedVPtime-VoicePieceCount*50)/RefVPTime - 1)
            if Scorce2<0:
                Scorce2 = 0
        elif DValue < 0:         
            AECResult = u'有压制' 
            Scorce1 = float(('%.2f' %(VPAllStrLen/RefVLen)))  
            Scorce2 = float(('%.2f' %(CookedVPtime/RefVPTime)))  
        else:
            AECResult = u'效果良好'
            Scorce1 = 1.0
            Scorce2 = 1.0
        #语音残留片段
        a = (float(Scorce1),float(Scorce2))
        average = 5*(np.average(a,weights=[8,2]))
        ScorceList = str(Scorce1)+' '+str(Scorce2)
        #print average,ScorceList
        VoicePieceList=str(VoicePieceList).replace(',','') 
        Result = ''.join(TestTime+','+AECResult+','+PCMPath+','+str(PeakdB)+','+str(CookedVPtime)+','+str(RefVPTime)+','+str(AECVPTimePercent)+','+VoicePieceList+','
                         +str(AllGreaterThanMinidBTime)+','+str(RefTime)+','+str(AECFailPercent)+','+
                         VRRestult+','+str(VPAllStrLen)+','+str(RefVLen))
        WriteTestResult(TestResultFileName, ResultHead, Result)
    end = time.time()
    print end-start,'s'

#调试
if __name__ == "__main__": 
    #PCMPath=r"FB_male_female_single-talk_seq_lianxu.pcm"
    PCMPath = r"D:\AEC_sop\CapAudio_all\Cap_Audio_file1\2018_01_23_20_04_00\capaec8.pcm"
    #PCMPath = r"D:\AEC_sop\CapAudio_all\Cap_Audio_file_123\2018_01_22_17_41_10\capaec0.pcm"
    SampleRate=48000
    MinidB=-55
    RefVPTime=28419
    RefTime=22155
    RefPeakdB=-8
    RefVLen=52
    AECMod='d'
    AECResultAutoAnalysis(PCMPath,SampleRate,MinidB,RefVPTime,RefTime,RefPeakdB,RefVLen,AECMod)


    
