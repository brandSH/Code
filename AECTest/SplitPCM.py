# -*- coding: GBK -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#��һ��PCM�ָ������Ƭ

#---��չ---
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
#����Ĭ�ϱ����ʽΪutf-8
reload(sys)  
sys.setdefaultencoding('utf-8') 

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

#��ȡ��������������Ƭ��ʼ����ID�����ȡ�ÿƬ���������dB������
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
                    VoicePieceList.append ((VoicePieceStartIndex, (VoicePieceEndIndex - VoicePieceStartIndex) , VoicePiecePeakdB))    #��ʼID��ʱ�������dB
                    VoicePiecePeakdB = -1000
                    VoicePieceStartIndex = i
                if VoicePiecePeakdB < PCMdBList[i]:
                    VoicePiecePeakdB = PCMdBList[i]                    
            VoicePieceSampleIndex = i       
    VoicePieceList.append ((VoicePieceStartIndex, (VoicePieceSampleIndex - VoicePieceStartIndex) , VoicePiecePeakdB))
    return(VoicePieceList)     
 
 #�ָ�����Ƭ   
def SplitPCM(PCMPath,SampleRate,VoiceList):
    PCMBytes = open(PCMPath,'rb')
    for i in range(len(VoiceList)):
        #������Ƭʱǰ����������
        PCMBytes.seek(VoiceList[i][0] * 2 - SampleRate * 0.2 , 0)   
        PCMPiece = PCMBytes.read(VoiceList[i][1] * 2 + SampleRate * 0.2)   
        PCMPieceFile = open(str(i + 1) + '.pcm','w')
        PCMPieceFile = open(str(i + 1) + '.pcm','rb+')  #����ʹ�ö����ƴ�
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
