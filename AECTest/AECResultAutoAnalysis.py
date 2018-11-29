# -*- coding: GBK -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#�����ܺ�����AECResultAutoAnalysis()

#Ŀǰ��֧��16bit������ȵ�����
#�ð汾�����˶�AEC��������ʧЧʱ�Ľ��ͨ��ͳ�ƻ��������������ȡ���������������
#���Խ����AECģʽ��Ϊ�����ļ���SingleTalk.csv    DoubleTalk.csv
#SingleTalk.csv�ֶΣ�TestTime,Result,Cooked,PeakdB,CookedTime,RefTime,Cooked/RefTime*100%,MaxVPTime,MaxVPTimedB,MiniVPTime,MiniVPTimedB,MaxVPdB,MaxVPdBTime,MiniVPdB,MiniVPdBTime,AVGVPTime,AVGVPdB,VPCount
#DoubleTalk.csv�ֶΣ�TestTime,Result,Cooked,PeakdB,CookedTime,RefTime,Cooked/RefTime*100%
#VP: VoicePiece  

#-----2017-8-29-----
#��������ʶ���ܣ�������ʱ��Ҫ����Internet������
#�轫�ű�VoiceRecognition�ŵ���ͬĿ¼��
#�޸�AECResultAutoAnalysis()�ӿ�Ϊ��AECResultAutoAnalysis(PCMPath,SampleRate,MinidB,RefTime,RefPeakdB,RefVLen,AECMod)
#˫�����ж���������ΪAEC���ʶ�����ָ���
#����.csv�ֶΣ���������ʶ������Cook���ָ�����Ref���ָ�������
#SingleTalk.csv�ֶΣ�TestTime,Result,Cooked,PeakdB,CookedTime,RefTime,Cooked/RefTime*100%,MaxVPTime,MaxVPTimedB,MiniVPTime,MiniVPTimedB,MaxVPdB,MaxVPdBTime,MiniVPdB,MiniVPdBTime,AVGVPTime,AVGVPdB,VPCount,VRRestult,CookVLen,RefVLen
#DoubleTalk.csv�ֶΣ�TestTime,Result,Cooked,PeakdB,CookedTime,RefTime,Cooked/RefTime*100%,VRRestult,CookVLen,RefVLen

#---��չ---
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import division
import os
import sys
import math
import time
import multiprocessing
import VoiceRecognition


#��ȡPCM��dB�б�
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
        
        if SampleValueHByte >= 128: #�Ƿ�Ϊ����
            SampleValueH = SampleValueHByte * 256
            dBList.append(int(20*math.log10(abs(SampleValueL+SampleValueH-65536)/32767)))
        else:   #�Ƿ�Ϊ������0
            SampleValueH = SampleValueHByte * 256
            if SampleValueL + SampleValueH == 0:
                dBList.append(-1000)       #ʹ��-1000��ʾ��������С
            else:                
                dBList.append(int(20*math.log10((SampleValueL+SampleValueH)/32767)))
    PCMBytes.close()
    return dBList  

#��ȡPCM����MinidB��ʱ�������dBֵ��ƽ��dBֵ
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

#��ȡ��������������Ƭ���ȡ�ÿƬ���������dB������
def GetVoiceList(PCMdBList,SampleRate,MinidB):
    VPInterval = SampleRate // 5    #�Դ���200ms��Ϊ����Ƭ�ָ�ļ��
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

#���ǵ�˫��AEC��������������ܷ����ı䣬���MinidB��Ҫ������
def DoubleTalkPCMGreaterThanMinidBTime(PCMdBList,SampleRate,MinidB,RefPeakdB):
    PeakdB = max(PCMdBList)
    MinidB = MinidB - (RefPeakdB - PeakdB)
    (AllGreaterThanMinidBTime,PeakdB,AVGdB) = PCMGreaterThanMinidBTime(PCMdBList, SampleRate, MinidB)
    return (AllGreaterThanMinidBTime,PeakdB,AVGdB)   

#д���
def WriteTestResult(TestResultFileName,ResultHead,Result):    
    if os.path.exists(TestResultFileName) == False:
        TestResultFile = open(TestResultFileName,'w')
        TestResultFile.write(ResultHead+'\n'+Result)
    else: 
        TestResultFile = open(TestResultFileName,'a')
        TestResultFile.write('\n'+Result)                 
    TestResultFile.close()    

#AEC����Զ�Ԥ��
#RefTime �ο����д���MinidB�������������ʱ��
#RefVLen �ο����������ֵĸ���
#PCMPath���ܻ��пո�
def AECResultAutoAnalysis(PCMPath,SampleRate,MinidB,RefTime,RefPeakdB,RefVLen,AECMod):
    start = time.time()
    PCMdBList = getdBList(PCMPath, SampleRate)        
    TestTime = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    FFMPEG=multiprocessing.Process(target=os.system,args=('.\\ffmpeg.exe  -f s16le -ar '+str(SampleRate)+' -ac 1 -i '+PCMPath+' -acodec pcm_s16le -ar 8000 out.wav -y',))
    FFMPEG.daemon=True
    FFMPEG.start()  
    FFMPEG.join()
    (VRRestult, VPAllStrLen) = VoiceRecognition.VoiceRecognition('out.wav')
    #����
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
            MaxVPTime = VoicePieceList[VoicePieceCount-1][0]   #VP: VoicePiece   ��ȡ�ʱ��Ƭ����       
            MaxVPTimedB = VoicePieceList[VoicePieceCount-1][1]      #�ʱ��Ƭ�����dB
            VoicePieceList.sort(key = lambda x:(x[0],-x[1]))    #����Ԫ��ĵ�һ����Ƭʱ�䣩��С��������,�����һ����ͬ,����Ԫ���2����Ƭ���dB���Ӵ�С���򣬴Ӷ����Եõ�ʱ����С����������Ƭ
            MiniVPTime = VoicePieceList[0][0]   #���ʱ��Ƭ����
            MiniVPTimedB = VoicePieceList[0][1]     #���ʱ��Ƭ�����dB
            VoicePieceList.sort(key = lambda x:x[1])    #��dB��С����������dB��ͬ��Ƭʱ�䰴��С��������
            MaxVPdB = VoicePieceList[VoicePieceCount-1][1]      #���dB
            MaxVPdBTime = VoicePieceList[VoicePieceCount-1][0]      #���dB����ʱ��Ƭ�ĳ���
            VoicePieceList.sort(key = lambda x:(x[1],-x[0]))    #����Ԫ��ĵ�2����Ƭ���dB����С��������,�����2����ͬ,����Ԫ���1����Ƭʱ�䣩�Ӵ�С���򣬴Ӷ����Եõ�������С��ʱ�����Ƭ
            MiniVPdB = VoicePieceList[0][1]     #��СdB
            MiniVPdBTime = VoicePieceList[0][0]     #��СdB����ʱ��Ƭ�ĳ���
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
    #˫��
    elif AECMod == 'd' or AECMod =='D':
        (AllGreaterThanMinidBTime,PeakdB,AVGdB) = DoubleTalkPCMGreaterThanMinidBTime(PCMdBList,SampleRate,MinidB,RefPeakdB)
        AECFailPercent = (AllGreaterThanMinidBTime / RefTime) * 100
        TestResultFileName = 'DoubleTalk.csv'
        ResultHead = 'TestTime,Result,Cooked,PeakdB,CookedTime,RefTime,Cooked/RefTime*100%,VRRestult,CookVLen,RefVLen'
        DValue = VPAllStrLen - RefVLen
        if DValue > 0:
            AECResult = 'F'            
        elif DValue < 0:         
            AECResult = '��ѹ��'            
        else:
            AECResult = 'Ч������'
        Result = ''.join(TestTime+','+AECResult+','+PCMPath+','+str(PeakdB)+','+str(AllGreaterThanMinidBTime)+','+str(RefTime)+','+str(AECFailPercent)+','+
                         VRRestult.replace(',','|')+','+str(VPAllStrLen)+','+str(RefVLen))
        WriteTestResult(TestResultFileName, ResultHead, Result)
    end = time.time()
    print end-start,'s'

#����
if __name__ == "__main__": 
    #PCMPath = '.\\˫��\\��Ϊ\\����\\��Ϊ����.pcm'
    PCMPath = '48K����˫��.pcm'
    SampleRate = 48000
    MinidB = -60
    RefTime = 500000
    RefPeakdB = -5
    RefVLen = 144
    AECMod = 'd'
    AECResultAutoAnalysis(PCMPath,SampleRate,MinidB,RefTime,RefPeakdB,RefVLen,AECMod)    
    print 'Over!'
    
    
