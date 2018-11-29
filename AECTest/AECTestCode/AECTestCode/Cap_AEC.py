# -*- coding: utf-8 -*-
import getpass,datetime
import time
import telnetlib
import subprocess
import string
import os
import ftplib 
from sys import argv
import csv
import re
import codecs
import wave
import shutil
import ConfigParser
import threading
import logging  
import AECResultAutoAnalysis
import VoiceRecognition
import GetVoiceList
import ExceptionHandling
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#继承重写ConfigParser，解决大小写问题
class MyConfigParser(ConfigParser.ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr

#日志模块
logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='test.log',  
                    filemode='a') 
#logging.debug('debug message')  
#logging.info('info message')  
#logging.warning('warning message')  
#logging.error('error message')  
#logging.critical('critical message')  

#NTP时间同步模块
def NTPTime(NTPServerIP):
		try:
			commandref="ntpdate -b " + NTPServerIP
			var = os.popen(commandref)
			NTPstr=var.read(500)
			if NTPstr.index(" step time server " + NTPServerIP +" offset"):
				NTPstr=NTPstr.split()
				delytime=NTPstr[NTPstr.index('offset')+1]
				logging.info("step time server " + NTPServerIP + " offset " + delytime + " sec") 
				print delytime
		except:
			print "NTP failed!"
        #print "sucess!"

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

#读取"OnlyReadConfig.ini"配置函数
def Get_OnlyReadConfig(configfile):
        cf = MyConfigParser()
        cf.read(configfile)
        OriDictTestFile = cf.get("TestFileValua", "OriDictTestFile")
        return OriDictTestFile

#创建文件夹函数
def MakeDirs(CapPath):
        isExists=os.path.exists(CapPath)
        if not isExists:
                os.makedirs(CapPath)

#获取文件函数
def Get_ref_file(path_ref_file):
    i=0
    RefTestFileList=[]
    for root, dirs, files in os.walk(path_ref_file):
        for ref_name in files:
                if ref_name.endswith(".wav"):
                        #print (ref_name)
                        RefTestFileList.append(ref_name)
                        i=i+1
    return RefTestFileList

#计算有效声音片段时间、有效声音时间、峰值dB和语音识别个数等
#RefVPTime,RefTime,RefPeakdB,ResultStrLen
def CallParameter(MinidB,RefPcmPath):
        #wavfilelist=Get_ref_file(path_ref_file)
        #path1 = wavpath + wavfilelist[i]
        isExists=os.path.exists("output.pcm")
        if isExists:
                os.remove("output.pcm")
        #print RefPcmPath
        command1 = "ffmpeg -i "+ RefPcmPath+" -f s16le -ar 48000 -acodec pcm_s16le output.pcm"
        subprocess.call(command1)
        #subprocess.call('AECResultAutoAnalysis.exe output.pcm 48000 '+ MinidB)
        PCMdBList = GetVoiceList.getdBList("output.pcm", 48000)
        (VoiceList,VoiceRefTimePeakdB) = GetVoiceList.GetVoiceList(PCMdBList, 48000, int(MinidB))
        commandref="AECResultAutoAnalysis.exe output.pcm 48000 "+ str(MinidB)
        var = os.popen(commandref)
        str1=var.read(100)
        str1 = re.findall(r"\d+\.?\d*",str1)
        #print str
        RefTime = str1[1]
        RefVPTime = VoiceRefTimePeakdB[0]
        RefPeakdB = VoiceRefTimePeakdB[2]
        #------计算语音识别字数-------#
        isExists=os.path.exists("output.wav")
        if isExists:
                os.remove("output.wav")
        command2 = "ffmpeg -i "+ RefPcmPath+" -f s16le -ar 8000 -acodec pcm_s16le output.wav"
        subprocess.call(command2)
        (ResultStr,ResultStrLen) = VoiceRecognition.VoiceRecognition("output.wav")
        ResultStrLen=ResultStrLen
        #print ResultStrLenList
        return (RefVPTime,RefTime,RefPeakdB,ResultStrLen)

#参考测试序列名称及有效语音时间、峰值dB、语音识别字数数据
def DictTestFileValua(path_ref_file,MinidB):
        UpDateDictTestFile={}
        OriDictTestFile=Get_OnlyReadConfig('OnlyReadConfig.ini')
        OriDictTestFile=eval(OriDictTestFile)
        #OriDictTestFile={'FB_male_female_single-talk_seq_xing.pcm':55,
                         #'FB_male_female_single-talk_seq_lianxu.pcm':145}
        #print OriDictTestFile
        RefTestFile=Get_ref_file(path_ref_file)
        for i in range(len(RefTestFile)):
                RefTestFilePath = path_ref_file + RefTestFile[i]
                print RefTestFilePath
                (RefVPTime,RefTime,RefPeakdB,ResultStrLen) = CallParameter(MinidB,RefTestFilePath)
                if OriDictTestFile.has_key(RefTestFile[i]):
                        OriResultStrLen=OriDictTestFile[RefTestFile[i]]
                        PcmRefVoiceLen=max(int(OriResultStrLen),int(ResultStrLen))
                else:
                        PcmRefVoiceLen=ResultStrLen
                UpDateDictTestFile.setdefault(RefTestFile[i],[]).append(int(RefVPTime))
                UpDateDictTestFile.setdefault(RefTestFile[i],[]).append(int(RefTime))
                UpDateDictTestFile.setdefault(RefTestFile[i],[]).append(int(RefPeakdB))
                UpDateDictTestFile.setdefault(RefTestFile[i],[]).append(int(PcmRefVoiceLen))
                OriDictTestFile[RefTestFile[i]]=int(PcmRefVoiceLen)
        #-----修改配置文件--------#
        cf = MyConfigParser()
        cf.read('OnlyReadConfig.ini')
        cf.sections()
        cf.items("TestFileValua")  
        cf.set('TestFileValua', 'OriDictTestFile', OriDictTestFile)
        cf.write(open('OnlyReadConfig.ini', 'w'))
        #print OriDictTestFile
        return UpDateDictTestFile
        
#Telnet模块
def TelnetMudolar(MT_IP,Tel_Port,Tel_UN,Tel_PW,Tel_Command):
        #调用：TelnetMudolar(MT_IP,Tel_Port,Tel_UN,Tel_PW,Tel_Command)
        try:
                tn = telnetlib.Telnet(MT_IP,Tel_Port)
                tn.write(Tel_UN + "\r\n")
                tn.write(Tel_PW + "\r\n")
                tn.write(Tel_Command + "\r\n")
                print (Tel_Command)
                tn.close()
        except:
                logging.error('Telnet失败，请确保网络通畅或检查数据后重试')
                sys.exit(1)

        
#FTP模块取文件
def FTPMudolar(i,MT_IP,Ftp_UN,Ftp_PW,FTP_FilePath,path_ftp,FTP_FileNameList):
        #调用：FTPMudolar(i,MT_IP,FTP_UN,FTP_PW,FTP_FilePath,path_ftp,FTP_FileNameList)
        #------------------登陆FTP-----------------#
        try:
                ftp=ftplib.FTP()
                ftp.connect(MT_IP)
                ftp.login(Ftp_UN,Ftp_PW)
                print ftp.getwelcome()
        except:
                logging.error('登录FTP失败，请确保网络通畅或检查IP、用户名和密码后重试')
                sys.exit(1)
        try:
                FTP_FilePath = '/' + FTP_FilePath + '/'
                ftp.cwd(FTP_FilePath)
                bufsize=1024
                #--------------------取文件--------------------#
                #path_ftp = path + "\\" + time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
                for q in range(len(FTP_FileNameList)):
                        FileShotName = os.path.splitext(FTP_FileNameList[q])[0]
                        FTP_FileName = FTP_FileNameList[q]
                        ReFTP_FileName = FileShotName + str(i) + '.pcm'
                        strFileName =  path_ftp  + '\\'+ ReFTP_FileName
                        fp = open(strFileName,'wb')
                        ftp.rename(FTP_FileName, ReFTP_FileName)
                        ftp.retrbinary('RETR ' + ReFTP_FileName, fp.write, bufsize)
                        ftp.rename(ReFTP_FileName, FTP_FileName )
                        fp.close()
        except:
		logging.error('FTP取文件失败，请确保网络通畅或检查文件路径和文件名后重试')
                sys.exit(1)

#创建AEC处理模块线程
def AECAnalysis(i,RefTestFileList,UpDateDictTestFile,strFileCapAecName,MinidB,AECMod):
	try:
		n=int(i)%len(RefTestFileList)
		RefVPTime = UpDateDictTestFile[RefTestFileList[n]][0]
		RefTime = UpDateDictTestFile[RefTestFileList[n]][1]
		RefPeakdB = UpDateDictTestFile[RefTestFileList[n]][2]
		RefVLen = UpDateDictTestFile[RefTestFileList[n]][3]
		logging.info(strFileCapAecName + 'AEC自动化处理参数为RefVPTime:%s RefTime:%s RefPeakdB:%s RefVLen:%s'%(RefVPTime,RefTime,RefPeakdB,RefVLen) )
                AECResultAutoAnalysis.AECResultAutoAnalysis(strFileCapAecName,48000,int(MinidB),RefVPTime,RefTime,RefPeakdB,RefVLen,AECMod)
        except:
                logging.error(strFileCapAecName + '分析失败，请确保网络通畅或检查数据后重试')
                sys.exit(1)
        print "over!"               
        
#定时启动函数            
def timerFun(sched_Timer):
        CapPath=os.getcwd() + "\\Cap_Audio_file"
        path_ref_file = os.getcwd() + "\\test_file\\"
        #返回配置文件参数 FTP_FileName字符串转List
        ConfigDict = Get_config("Config.ini")
        globals().update(ConfigDict)
        #print (Sched_Timer,Cycle_Num,Play_Interval,NTPServerIP,MinidB,AECMod)
        #print (IsKDMT,MT_IP,Tel_Port,Tel_UN,Tel_PW,Tel_Command,FTP_UN,FTP_PW,FTP_FilePath,FTP_FileName)
        FTP_FileNameList = [x for x in FTP_FileName.split(',')]
        #Necessary参数处理
        RefTestFileList = Get_ref_file(path_ref_file)
        NewCycle_Num=int(Cycle_Num) * len(RefTestFileList)
        print NewCycle_Num
        NewSched_Timer = datetime.datetime.strptime(Sched_Timer, "%Y-%m-%d %H:%M:%S")
        #计算参考测试序列有效声音时间、峰值dB和识别字数等
        UpDateDictTestFile=DictTestFileValua(path_ref_file,int(MinidB))
        #*--------------------------While循环模块--------------------------*
        i = 0
        while i<NewCycle_Num:
                #*-----------------定时模块--------------------------------*	
		now=datetime.datetime.now()
                exe = NewSched_Timer - now 
                a = exe.microseconds
                b = exe.seconds
                c = a/1000+b*1000
                d = c/1000
                print d
                if d>=2:
			time.sleep(1)
                else :
                        time.sleep(0.001)
                if  datetime.datetime.now() >= NewSched_Timer :		
			print datetime.datetime.now()    
		    #*-----------------Telnet模块-------------------*
			if int(IsKDMT)==1:
				P2 = threading.Thread(target=TelnetMudolar,args=(i,MT_IP,Tel_Port,Tel_UN,Tel_PW,Tel_Command,))
				P2.setDaemon(True)
				P2.start()
				#TelnetMudolar(MT_IP,Tel_Port,Tel_UN,Tel_PW,Tel_Command)
			#*-----------------时间同步模块----------------------*
			if int(ISNTPServer)==0:
				if (i%30)==0:
				        P4 = threading.Thread(target=NTPTime,args=(NTPServerIP,))
				        P4.setDaemon(True)
				        P4.start()				        
					#NTPTime(NTPServerIP)
			#*----------------音频采集---------------------------------*
			try:
				path_ftp = CapPath + "\\" + time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
			        os.makedirs(path_ftp)
			        strFileCapAecName =  path_ftp  +  '\\capaec' + str(i) + '.pcm' 	
			        strcmdcap = 'ffmpeg -f dshow -i audio=' + '\"线路输入 (Blackmagic DeckLink Mini Recorder 4K Audio)\"'+ ' -f s16le -acodec pcm_s16le -ar 48000 -ac 1 -t 45 '+ strFileCapAecName  
				strcmdcap = strcmdcap.encode('gbk')
			        subprocess.call(strcmdcap)
			        NewSched_Timer = NewSched_Timer + datetime.timedelta(seconds=int(Play_Interval))
			except:
				NewSched_Timer = NewSched_Timer + datetime.timedelta(seconds=int(Play_Interval))
			#*-----------------FTP取文件模块-----------------------------
			if int(IsKDMT)==1:
				P3 = threading.Thread(target=FTPMudolar,args=(i,MT_IP,FTP_UN,FTP_PW,FTP_FilePath,path_ftp,FTP_FileNameList,))
				P3.setDaemon(True)
				P3.start()
				#FTPMudolar(i,MT_IP,FTP_UN,FTP_PW,FTP_FilePath,path_ftp,FTP_FileNameList)
			#*------------------AEC效果自动预判-----------------------*
			P1=threading.Thread(target=AECAnalysis,args=(i,RefTestFileList,UpDateDictTestFile,strFileCapAecName,MinidB,AECMod,))
			P1.setDaemon(True)
			P1.start()
			i=i+1
    
           
#调试函数 
if __name__=='__main__':   
        path_ref_file = os.getcwd() + "\\test_file\\"
        ConfigDict = Get_config("Config.ini")
        Sched_Timer = ConfigDict.get('Sched_Timer')
        try:
                ExceptionHandling.EH_Get_config()
        except:
                print "请查看日志文件test.log"
                sys.exit(1)
        timerFun(Sched_Timer)
        print "Test over! Please check  the test results!"


