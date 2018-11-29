# -*- coding: cp936 -*-
import getpass,datetime
import time
import telnetlib
import subprocess
import AECResultAutoAnalysis_net
import VoiceRecognition
import string
import os
import ftplib 
from sys import argv
import csv
import re
import codecs
import wave
import shutil
import  ConfigParser
import multiprocessing

#读取配置文件
def Get_config(configfile):
    list=[]
    cf = ConfigParser.ConfigParser()
    cf.read(configfile)
    list.append(cf.getint("play","cycle_num"))
    list.append(cf.getint("play","play_year"))
    list.append(cf.getint("play","play_month"))
    list.append(cf.getint("play","play_day"))
    list.append(cf.getint("play","play_hour"))
    list.append(cf.getint("play","play_minute"))
    list.append(cf.getint("play","play_second"))
    list.append(cf.getint("play","play_interval"))
    list.append(cf.getint("cap","MinidB"))
    #list.append(cf.getint("cap","AECMod"))
    return list

#创建cap音频文件存放文件夹
def MakeDirs(CapPath):
        isExists=os.path.exists(CapPath)
        if not isExists:
                os.makedirs(CapPath)

#读取测试序列列表
def Get_ref_file(path_ref_file):
    i=0
    ref=[]
    for root, dirs, files in os.walk(path_ref_file):
        for ref_name in files:
            if ref_name.endswith(".wav"):
                #print (ref_name)
                ref.append(ref_name)
                i=i+1
    return ref
    
#计算参考测试序列有效残留时间、峰值dB及识别语音个数
def CallParameter(MinidB):
        wavpath=os.getcwd()+"\\voice\\"
        wavfilelist=[]
        PcmRefTime=[]
        PcmRefPeakdB=[]
        ResultStrLenList=[]
        wavfilelist=Get_ref_file(wavpath)
        for i in range(len(wavfilelist)):
                path1 = wavpath + wavfilelist[i]
                isExists=os.path.exists("output.pcm")
                if isExists:
                        os.remove("output.pcm")
                command1 = "ffmpeg -i "+ path1+" -f s16le -ar 48000 -acodec pcm_s16le output.pcm"
                print command1
                subprocess.call(command1)
                #subprocess.call('AECResultAutoAnalysis.exe output.pcm 48000 '+ MinidB)
                commandref="AECResultAutoAnalysis.exe output.pcm 48000 "+ str(MinidB)
                #subprocess.call(commandref)
                var = os.popen(commandref)
                str1=var.read(100)
                str1 = re.findall(r"\d+\.?\d*",str1)
                #print  str1
                PcmRefTime.append(str1[1])
                PcmRefPeakdB.append(str1[2])
                #------识别字数-------#
                FFMPEG=multiprocessing.Process(target=os.system,args=('.\\ffmpeg.exe  -f s16le -ar 48000 -ac 1 -i '+path1+' -acodec pcm_s16le -ar 8000 -ac 1 out.wav -y',))
                FFMPEG.daemon=True
                FFMPEG.start()  
                FFMPEG.join()
                (ResultStr, ResultStrLen) = VoiceRecognition.VoiceRecognition('out.wav')                
                #(ResultStr,ResultStrLen) = VoiceRecognition.VoiceRecognition(path1)
                ResultStrLenList.append(ResultStrLen)
                #print ResultStrLenList
        return (PcmRefTime,PcmRefPeakdB,ResultStrLenList)

#telnet模块
def TelnetMudolar(MT_IP,Tel_Port,Tel_Un,tel_pw):
        tn = telnetlib.Telnet(MT_IP,Tel_Port)
        tn.write(Tel_Un + "\r\n")
        tn.write(Tel_Pw + "\r\n")                
        Command1 = "saveaec 3000"
        tn.write(Command1 + "\r\n")
        print (Command1)
        tn.close()
        
#FTP取文件模块
def FTPMudolar(MT_IP,Ftp_Un,Ftp_Pw,Ftp_AECFilePath):
        #------------------ftp到aec端端口-----------------# 
        ftp=ftplib.FTP()        
        ftp.connect(MT_IP)      
        ftp.login(Ftp_Un,Ftp_Pw)
        print ftp.getwelcome()            
        ftp.cwd(Ftp_AECFilePath)                
        bufsize=1024
        #--------------------取ftp文件模块--------------------#
        #path_ftp = path + "\\" + time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
        
        strFileAecName =  path_ftp  +  '\\aec'+i+'.pcm'                
        fp = open(strFileAecName,'wb')    
        ftp.rename('aec.pcm', 'aec'+i+'.pcm') 
        ftp.retrbinary('RETR ''aec'+i+'.pcm''', fp.write, bufsize)  
        ftp.rename('aec'+i+'.pcm','aec.pcm' )     
        fp.close()                    
    
        strFileCapName =  path_ftp  +  '\\cap'+i+'.pcm'                
        fp = open(strFileCapName,'wb')     
        ftp.rename('cap.pcm', 'cap'+i+'.pcm')
        ftp.retrbinary('RETR ''cap'+i+'.pcm''', fp.write, bufsize)  
        ftp.rename('cap'+i+'.pcm','cap.pcm')     
        fp.close() 
    
        strFileRefName =  path_ftp  +  '\\ref'+i+'.pcm'                
        fp = open(strFileRefName,'wb')    
        ftp.rename('ref.pcm', 'ref'+i+'.pcm' ) 
        ftp.retrbinary('RETR ''ref'+i+'.pcm''', fp.write, bufsize)  
        ftp.rename('ref'+i+'.pcm','ref.pcm')     
        fp.close() 	


#定时采集              
def timerFun(sched_Timer,cycle_num,MinidB,play_interval):
        #计算参考测试序列有效残留时间和语音个数
        print "timerFun123456789"
        (PcmRefTime,PcmRefPeakdB,ResultStrLenList)=CallParameter(MinidB)
        print ResultStrLenList
        MakeDirs(CapPath)
        NoiseList = Get_ref_file(os.getcwd()+'//noise')
        #print len(NoiseList),len(PcmRefTime)
        cycle_num = cycle_num * int(len(NoiseList))*int(len(PcmRefTime))
        print cycle_num
        i =0
        while i<cycle_num:
                #*-----------------定时--------------------------------*
                now=datetime.datetime.now()
                exe = sched_Timer - now 
                a = exe.microseconds
                b = exe.seconds
                c = a/1000+b*1000
                d = c/1000
                print d
                if d>=2:
                        time.sleep(1)
                else :
                        time.sleep(0.001)
                if  datetime.datetime.now() >= sched_Timer : #当前时间>=设定时间		
                        print datetime.datetime.now()
                                                                
                        #*-----------------新建文件夹--------------------------------*
                        path_ftp = CapPath + "\\" + time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
                        os.makedirs(path_ftp )
                        strFileCapAecName =  path_ftp  +  '\\CapANS_' + str(i) + '.pcm' 					
                        #*-----------------采集音频---------------------------------*
                        strcmdcap = 'ffmpeg -f dshow -i audio=' + '\"线路输入 (Blackmagic DeckLink Mini Recorder 4K Audio)\"'+ ' -f s16le -acodec pcm_s16le -ar 48000 -ac 1 -t 45 '+ strFileCapAecName
                        print "strFileCapAecName"
                        print strFileCapAecName
                        subprocess.call(strcmdcap)
                        #------------------预判和处理音频文件-----------------------#
                        n=(int(i)//len(NoiseList))%(len(PcmRefTime))
                        #sched_Timer = sched_Timer+datetime.timedelta(seconds=play_interval)
                        try:
                            AECResultAutoAnalysis_net.AECResultAutoAnalysis(strFileCapAecName,48000,MinidB,int(PcmRefTime[n]),int(PcmRefPeakdB[n]),int(ResultStrLenList[n]),'d')
                        except:
                            print "pass"
                            #sched_Timer = sched_Timer+datetime.timedelta(seconds=play_interval)  
                            
                        sched_Timer = sched_Timer+datetime.timedelta(seconds=play_interval) 
                        i=i+1
                        
if __name__ == "__main__":                                                                
    #获取参数 给变量赋值      
    CapPath=os.getcwd() + "\\Cap_Audio_file"
    path_ref_file = os.getcwd() + "\\MixVoice\\"
    Get_ref_file(path_ref_file)
    config_list=Get_config('config.ini')
    cycle_num=config_list[0]
    play_interval=config_list[7]
    MinidB=config_list[8]
    #AECMode=config_list[9]
    sched_Timer = datetime.datetime(config_list[1],config_list[2],config_list[3],config_list[4],config_list[5],config_list[6],100000)
    print "start timerFun"
    timerFun(sched_Timer,cycle_num,MinidB,play_interval)
    print "Test over! Please check  the test results!"


