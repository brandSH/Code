# -*- coding: GBK -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#---周萍---
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import division
import os
import sys
import math
import time
import multiprocessing
#import VoiceRecognition
import numpy
import ConfigParser


#print sys.getdefaultencoding() 
#设置默认编码格式为utf-8
reload(sys)  
sys.setdefaultencoding('utf-8') 

#继承重写ConfigParser，解决大小写问题
class MyConfigParser(ConfigParser.ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr

#读取"Config.ini"配置函数
def Get_config(configfile):
    ConfigDict={}
    cf = MyConfigParser()
    cf.read(configfile)
    SectionList=cf.sections() 
    for x in range(len(SectionList)):
        ItemList=cf.items(SectionList[x])
        for z in range(len(ItemList)):
            #print ItemList[z][0],ItemList[z][1]
            ConfigDict[ItemList[z][0]]=ItemList[z][1]
    return ConfigDict

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
    VPInterval = SampleRate // 5   #以大于200ms作为声音片分割的间隔
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
                    VoicePieceList.append ((VoicePieceStartIndex, (VoicePieceEndIndex - VoicePieceStartIndex) , VoicePieceEndIndex))    #开始ID、时长、结束ID
                    VoicePiecePeakdB = -1000
                    VoicePieceStartIndex = i
                if VoicePiecePeakdB < PCMdBList[i]:
                    VoicePiecePeakdB = PCMdBList[i]                    
            VoicePieceSampleIndex = i       
    VoicePieceList.append ((VoicePieceStartIndex, (VoicePieceSampleIndex - VoicePieceStartIndex) ,VoicePieceSampleIndex))
    return(VoicePieceList)     
    
def SplitPCM(PCMPath,SampleRate,VoiceList):
    PCMBytes = open(PCMPath,'rb')
    for i in range(len(VoiceList)):
        PCMBytes.seek(VoiceList[i][0] * 2 - SampleRate * 0.5 , 0)
        PCMPiece = PCMBytes.read(VoiceList[i][1] * 2 + SampleRate * 1)
        PCMPieceFile = open(str(i + 1) + '.pcm','w')
        PCMPieceFile = open(str(i + 1) + '.pcm','rb+')  #必须使用二进制打开
        PCMPieceFile.write(PCMPiece)
        PCMPieceFile.close()
        
#获取不完整语音列表   
def Incomplete_ShortWord(PCMPath,SampleRate,VoiceList):
    VoiceTimeList=[]
    Incomplete_VoiceTimeList=[] 
    New_RefVoiceTimeList=[]
    RefVoiceTimeList = [493,418,420,564,473,453,390,516,447,554]
    for i in range(len(RefVoiceTimeList)):
        New_RefVoiceTime=RefVoiceTimeList[i]/2
        New_RefVoiceTimeList.append(New_RefVoiceTime)
        
    for i in range(len(VoiceList)):
        VoiceTime=VoiceList[i][1]/SampleRate * 1000
        VoiceTimeList.append(VoiceTime)
        
    for i in range(len(VoiceTimeList)):        
        if VoiceTimeList[i] < min(New_RefVoiceTimeList):           
            Loss = 1-VoiceTimeList[i]/min(New_RefVoiceTimeList)
            Incomplete_VoiceTimeList.append((i,VoiceTimeList[i],Loss))
    return(Incomplete_VoiceTimeList)

       
if __name__ == "__main__":   
    #读配置文件
    ConfigDict = Get_config("Config.ini")
    globals().update(ConfigDict)
    SampleRate = int(ConfigDict.get('SampleRate'))
    MinidB=int(ConfigDict.get('MinidB'))  
    
    VoiceList = GetVoiceList(getdBList(PCMPath, SampleRate), SampleRate, MinidB)
    VoiceCounts = len(VoiceList)        
    #SplitPCM(PCMPath, SampleRate, VoiceList)   
    
    Incomplete_VoiceTimeList = Incomplete_ShortWord(PCMPath,SampleRate,VoiceList) 
    
    print Incomplete_VoiceTimeList
    
    #将打印输出到txt文档
    f_result=open('MIX_Result.txt', 'w') 
    sys.stdout=f_result    
    print 'Total Voice Piece Counts: ' 
    print >> f_result,str(VoiceCounts)       
    
    if len(Incomplete_VoiceTimeList) > 0:
        print 'Incomplete Voice Pieces:'
        for i in range(len(Incomplete_VoiceTimeList)):    
            print >> f_result,str(Incomplete_VoiceTimeList[i][0]+1) + '.pcm  ' + '  Loss:' + '%.2f%%' %(Incomplete_VoiceTimeList[i][2]*100)
    else:
        print 'No Incomplete Voice Piece !'
    
    f_result.close() 
    
   
        
    

