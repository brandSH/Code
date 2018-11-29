# -*- coding: GBK -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#将一个PCM分割成声音片

#---王展---
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import division
import os
import sys
import math
import time
import multiprocessing
#import VoiceRecognition
import numpy


#print sys.getdefaultencoding() 
#设置默认编码格式为utf-8
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

#获取声音序列中声音片开始样本ID、长度、每片声音的最大dB的序列
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
                    VoicePieceList.append ((VoicePieceStartIndex, (VoicePieceEndIndex - VoicePieceStartIndex) , VoicePiecePeakdB))    #开始ID、时长、最大dB
                    VoicePiecePeakdB = -1000
                    VoicePieceStartIndex = i
                if VoicePiecePeakdB < PCMdBList[i]:
                    VoicePiecePeakdB = PCMdBList[i]                    
            VoicePieceSampleIndex = i       
    VoicePieceList.append ((VoicePieceStartIndex, (VoicePieceSampleIndex - VoicePieceStartIndex) , VoicePiecePeakdB))
    return(VoicePieceList)     
 
 #分割声音片   
def SplitPCM(PCMPath,SampleRate,VoiceList):
    PCMBytes = open(PCMPath,'rb')
    for i in range(len(VoiceList)):
        #切声音片时前后增加余量
        PCMBytes.seek(VoiceList[i][0] * 2 - SampleRate * 0.2 , 0)   
        PCMPiece = PCMBytes.read(VoiceList[i][1] * 2 + SampleRate * 0.2)   
        PCMPieceFile = open(str(i + 1) + '.pcm','w')
        PCMPieceFile = open(str(i + 1) + '.pcm','rb+')  #必须使用二进制打开
        PCMPieceFile.write(PCMPiece)
        PCMPieceFile.close()
        
if __name__ == "__main__": 
    PCMPath = 'APU2_10-100_8K.pcm'
    SampleRate = 8000
    MinidB = -60 
    VoiceList = GetVoiceList(getdBList(PCMPath, SampleRate), SampleRate, MinidB)
    print '(StartID, Time, MaxdB)'
    for i in VoiceList:
        print str(i)
    #print VoiceList
    VoiceCounts = len(VoiceList)
    print 'Voice Counts: ' + str(VoiceCounts)
    SplitPCM(PCMPath, SampleRate, VoiceList)
    print 'Split PCM over!'
