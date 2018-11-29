# -*- coding: GBK -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#---��չ---
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import division
import os
import sys
import math
import time
import multiprocessing
import VoiceRecognition
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

#��ȡ��������������Ƭ��ʼ����ID�����ȡ�ÿƬ��������dB������
def GetVoiceList(PCMdBList,SampleRate,MinidB):
    VPInterval = SampleRate // 5  #�Դ���200ms��Ϊ����Ƭ�ָ�ļ��
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
                    #if (1000 * (VoicePieceEndIndex - VoicePieceStartIndex) // SampleRate)>5:
                    VoicePieceList.append ((VoicePieceStartIndex, (1000 * (VoicePieceEndIndex - VoicePieceStartIndex) // SampleRate), VoicePiecePeakdB))    #��ʼID��ʱ�������dB
                    VoicePiecePeakdB = -1000
                    VoicePieceStartIndex = i 
                if VoicePiecePeakdB < PCMdBList[i]:
                    VoicePiecePeakdB = PCMdBList[i]                    
            VoicePieceSampleIndex = i
    
    #if (1000 * (VoicePieceSampleIndex - VoicePieceStartIndex) // SampleRate)>5:
    VoicePieceList.append ((VoicePieceStartIndex, (1000 * (VoicePieceSampleIndex - VoicePieceStartIndex) // SampleRate), VoicePiecePeakdB))
    #VoicePieceList.sort()
    #print VoicePieceList
    SumVPTime = 0
    SumVPdB = 0
    SumMaxVPdBList = []
    VoiceRefTimePeakdB = []
    for i in range(len(VoicePieceList)):
        SumVPTime = SumVPTime + VoicePieceList[i][1]
        SumVPdB = SumVPdB + VoicePieceList[i][2]
        SumMaxVPdBList.append(VoicePieceList[i][2])
    #print SumMaxVPdBList
    SumMaxVPdB = SumMaxVPdBList[int(SumMaxVPdBList.index(max(SumMaxVPdBList)))]
    VoiceRefTimePeakdB.append(SumVPTime)
    VoiceRefTimePeakdB.append(SumVPdB)
    VoiceRefTimePeakdB.append(SumMaxVPdB)
    return(VoicePieceList,VoiceRefTimePeakdB)     
    
if __name__ == "__main__":
   PCMPath = r'FB_male_female_single-talk_seq_lianxu.pcm'
   #PCMPath = 'output.pcm'
   SampleRate = 48000
   MinidB = -50
   (VoicePieceList,VoiceRefTimePeakdB) = GetVoiceList(getdBList(PCMPath, SampleRate), SampleRate, MinidB)
   print VoicePieceList
   print VoiceRefTimePeakdB
   print 'Over!'
