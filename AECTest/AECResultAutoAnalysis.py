# -*- coding: GBK -*-
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
import sys
import math
import time
import multiprocessing
import VoiceRecognition


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
            if GreaterThanMinidBCount <> 0:
                GreaterThanMinidBCountList.append(GreaterThanMinidBCount)
                GreaterThanMinidBCount = 0
                
    PeakdB = max(PCMdBList)
    AllGreaterThanMinidBTime = 0
    AllGreaterThanMinidBCount = 0
    AVGdB = 0
    for i in range(len(GreaterThanMinidBCountList)):
        AllGreaterThanMinidBTime = AllGreaterThanMinidBTime + (GreaterThanMinidBCountList[i] / SampleRate) * 1000
        AllGreaterThanMinidBCount = AllGreaterThanMinidBCount + GreaterThanMinidBCountList[i]
    if AllGreaterThanMinidBCount <> 0:        
        AVGdB = dBSum / AllGreaterThanMinidBCount
    else:
        AVGdB = -1000
    return (int(AllGreaterThanMinidBTime),PeakdB,int(AVGdB))

#获取声音序列中声音片长度、每片声音的最大dB的序列
def GetVoiceList(PCMdBList,SampleRate,MinidB):
    VPInterval = SampleRate // 5    #以大于200ms作为声音片分割的间隔
    VoicePieceStartIndex = 0
    VoicePieceEndIndex = 0
    VoicePieceSampleIndex = 0
    VoicePiecePeakdB = -1000
    FirstVoicePieceYorN = True
    VoicePieceList = []
    for i in range(len(PCMdBList)):
        if PCMdBList[i] > MinidB:            
            if FirstVoicePieceYorN == True:
                VoicePieceStartIndex = i 
                VoicePiecePeakdB = PCMdBList[i]
                FirstVoicePieceYorN = False
            else:              
                if i - VoicePieceSampleIndex > VPInterval:
                    VoicePieceEndIndex = VoicePieceSampleIndex
                    VoicePieceList.append(((1000 * (VoicePieceEndIndex - VoicePieceStartIndex) // SampleRate),VoicePiecePeakdB))
                    VoicePiecePeakdB = -1000
                    VoicePieceStartIndex = i
                if VoicePiecePeakdB < PCMdBList[i]:
                    VoicePiecePeakdB = PCMdBList[i]                    
            VoicePieceSampleIndex = i       
    VoicePieceList.append(((1000 * (VoicePieceSampleIndex - VoicePieceStartIndex) // SampleRate),VoicePiecePeakdB))
    return(VoicePieceList)         

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

#AEC结果自动预判
#RefTime 参考序列大于MinidB的所有样本点的时间
#RefVLen 参考序列中文字的个数
#PCMPath不能还有空格
def AECResultAutoAnalysis(PCMPath,SampleRate,MinidB,RefTime,RefPeakdB,RefVLen,AECMod):
    start = time.time()
    PCMdBList = getdBList(PCMPath, SampleRate)        
    TestTime = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    FFMPEG=multiprocessing.Process(target=os.system,args=('.\\ffmpeg.exe  -f s16le -ar '+str(SampleRate)+' -ac 1 -i '+PCMPath+' -acodec pcm_s16le -ar 8000 out.wav -y',))
    FFMPEG.daemon=True
    FFMPEG.start()  
    FFMPEG.join()
    (VRRestult, VPAllStrLen) = VoiceRecognition.VoiceRecognition('out.wav')
    #单讲
    if AECMod == 's' or AECMod =='S':
        (AllGreaterThanMinidBTime,PeakdB,AVGdB) = PCMGreaterThanMinidBTime(PCMdBList,SampleRate,MinidB)
        AECFailPercent = (AllGreaterThanMinidBTime / RefTime) * 100
        TestResultFileName = 'SingleTalk.csv' 
        ResultHead = 'TestTime,Result,Cooked,PeakdB,CookedTime,RefTime,Cooked/RefTime*100%,MaxVPTime,MaxVPTimedB,MiniVPTime,MiniVPTimedB,MaxVPdB,MaxVPdBTime,MiniVPdB,MiniVPdBTime,AVGVPTime,AVGVPdB,VPCount,VRRestult,CookVLen,RefVLen'
        if AllGreaterThanMinidBTime > 50 or PeakdB > -20:
            AECResult = 'F'
            VoicePieceList = GetVoiceList(PCMdBList,SampleRate,MinidB)
            VoicePieceCount = len(VoicePieceList)
            VoicePieceList.sort()
            MaxVPTime = VoicePieceList[VoicePieceCount-1][0]   #VP: VoicePiece   获取最长时间片长度       
            MaxVPTimedB = VoicePieceList[VoicePieceCount-1][1]      #最长时间片的最大dB
            VoicePieceList.sort(key = lambda x:(x[0],-x[1]))    #按照元组的第一个（片时间）从小到大排序,如果第一个相同,则按照元组第2个（片最大dB）从大到小排序，从而可以得到时间最小但声音最大的片
            MiniVPTime = VoicePieceList[0][0]   #最短时间片长度
            MiniVPTimedB = VoicePieceList[0][1]     #最短时间片的最大dB
            VoicePieceList.sort(key = lambda x:x[1])    #按dB从小到大排序，若dB相同，片时间按从小到大排序
            MaxVPdB = VoicePieceList[VoicePieceCount-1][1]      #最大dB
            MaxVPdBTime = VoicePieceList[VoicePieceCount-1][0]      #最大dB所在时间片的长度
            VoicePieceList.sort(key = lambda x:(x[1],-x[0]))    #按照元组的第2个（片最大dB）从小到大排序,如果第2个相同,则按照元组第1个（片时间）从大到小排序，从而可以得到声音最小但时间最长的片
            MiniVPdB = VoicePieceList[0][1]     #最小dB
            MiniVPdBTime = VoicePieceList[0][0]     #最小dB所在时间片的长度
            SumVPTime = 0
            SumVPdB = 0
            for i in range(VoicePieceCount):
                SumVPTime = SumVPTime + VoicePieceList[i][0]
                SumVPdB = SumVPdB + VoicePieceList[i][1]
            AVGVPTime = SumVPTime // VoicePieceCount
            AVGVPdB = SumVPdB // VoicePieceCount                       
            Result = ''.join(TestTime+','+AECResult+','+PCMPath+','+str(PeakdB)+','+str(AllGreaterThanMinidBTime)+','+str(RefTime)+','+str(AECFailPercent)+','
                              +str(MaxVPTime)+','+str(MaxVPTimedB)+','+str(MiniVPTime)+','+str(MiniVPTimedB)+','+str(MaxVPdB)+','+str(MaxVPdBTime)+','+str(MiniVPdB)+
                              ','+str(MiniVPdBTime)+','+str(AVGVPTime)+','+str(AVGVPdB)+','+str(VoicePieceCount)+','+VRRestult.replace(',','|')+','+str(VPAllStrLen)+','+str(RefVLen))
            WriteTestResult(TestResultFileName, ResultHead, Result)
        else:
            AECResult = 'P'
            Result = ''.join(TestTime+','+AECResult+','+PCMPath+','+str(PeakdB)+','+str(AllGreaterThanMinidBTime)+','+str(RefTime)+','+str(AECFailPercent)+','*12+
                              VRRestult.replace(',','|')+','+str(VPAllStrLen)+','+str(RefVLen))
            WriteTestResult(TestResultFileName, ResultHead, Result)
    #双讲
    elif AECMod == 'd' or AECMod =='D':
        (AllGreaterThanMinidBTime,PeakdB,AVGdB) = DoubleTalkPCMGreaterThanMinidBTime(PCMdBList,SampleRate,MinidB,RefPeakdB)
        AECFailPercent = (AllGreaterThanMinidBTime / RefTime) * 100
        TestResultFileName = 'DoubleTalk.csv'
        ResultHead = 'TestTime,Result,Cooked,PeakdB,CookedTime,RefTime,Cooked/RefTime*100%,VRRestult,CookVLen,RefVLen'
        DValue = VPAllStrLen - RefVLen
        if DValue > 0:
            AECResult = 'F'            
        elif DValue < 0:         
            AECResult = '有压制'            
        else:
            AECResult = '效果良好'
        Result = ''.join(TestTime+','+AECResult+','+PCMPath+','+str(PeakdB)+','+str(AllGreaterThanMinidBTime)+','+str(RefTime)+','+str(AECFailPercent)+','+
                         VRRestult.replace(',','|')+','+str(VPAllStrLen)+','+str(RefVLen))
        WriteTestResult(TestResultFileName, ResultHead, Result)
    end = time.time()
    print end-start,'s'

#调试
if __name__ == "__main__": 
    #PCMPath = '.\\双讲\\华为\\连续\\华为连续.pcm'
    PCMPath = '48K连续双讲.pcm'
    SampleRate = 48000
    MinidB = -60
    RefTime = 500000
    RefPeakdB = -5
    RefVLen = 144
    AECMod = 'd'
    AECResultAutoAnalysis(PCMPath,SampleRate,MinidB,RefTime,RefPeakdB,RefVLen,AECMod)    
    print 'Over!'
    
    
