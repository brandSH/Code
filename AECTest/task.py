#coding: utf-8 
import getpass,datetime
import time
import telnetlib
import subprocess
import string
import os
import ConfigParser 
import ftplib 
from sys import argv
import csv
import re
import codecs
import pyaudio
import wave
import shutil

def task(mt,mode,host,port,tel_un,tel_pw,ftp_un,ftp_pw,H,M,S,MS,ref_file,aud_device):
    #------------------------从界面返回参数---------------------#
    host = str(host)
    port = str(port)
    ftp_un = str(ftp_un)
    ftp_pw = str(ftp_pw)
    tel_un = str(tel_un)
    tel_pw = str(tel_pw)    
    H = int(H)
    M = int(M)
    S = int(S)
    MS = int(MS)    
    ref_file = str(ref_file)
    aud_device = str(aud_device)
    print mt
    print mode
    print host
    print port
    print tel_un
    print tel_pw
    print ftp_un
    print ftp_pw
    print H
    print M
    print S
    print MS
    print ref_file     
    print aud_device
    #---------获取ref_file的ref时间模块-----------# 
    commandref='D:\\AEC_Auto_test\\AECResultAutoAnalysis.exe ' + 'D:\\AEC_Auto_test\\ref_file\\' + ref_file + ' 48000 -60' 
    #subprocess.call(commandref)
    var = os.popen(commandref)
    str1=var.read(100)
    print  str1
    str1 = re.findall(r"\d+\.?\d*",str1)
    ref = str1[1]
    #------------------wav播放模块-----------------# 
    def wave_PLAY():
        chunk = 1024
        f = wave.open("D:\\AEC_Auto_test\\ref_file\\" + ref_file ,"rb")
        p = pyaudio.PyAudio()
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),
        rate = f.getframerate(),
            output = True)
        data = f.readframes(chunk)
        while data != '':
            stream.write(data)
            data = f.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()    
    #------------------------同步定时模块------------------------# 
    if mt==0 :
        def timerFun(sched_Timer): 
            i = 1
            while True:
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
                if  datetime.datetime.now() >= sched_Timer :		
                    tn = telnetlib.Telnet(host,port)
                    tn.write(tel_un + "\r\n")
                    tn.write(tel_pw + "\r\n")                
                    Command1 = "saveaec 3000"
                    tn.write(Command1 + "\r\n")
                    print (Command1)
                    tn.close()
                    print datetime.datetime.now()
                    print "wave_PLAY()"
                    #time.sleep(2)
                    wave_PLAY()
                #------------------ftp到aec端端口-----------------# 
                    ftp=ftplib.FTP()        
                    ftp.connect(host)      
                    ftp.login(ftp_un,ftp_pw)
                    print ftp.getwelcome()            
                    ftp.cwd("/ramdisk/")                
                    bufsize=1024
                #--------------------取ftp文件模块--------------------#
                    time.sleep(20)
                    i=str(i)
                    path_ftp = "D:\\AEC_Auto_test\\test_result\\" + time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
                    os.mkdir(path_ftp )
                    strFileAecName =  path_ftp  +  '\\aec'+i+'.pcm'                
                    fp = open(strFileAecName,'wb')    
                    ftp.rename('aec.pcm', 'aec'+i+'.pcm') 
                    ftp.retrbinary('RETR ''aec'+i+'.pcm''', fp.write, bufsize)  
                    ftp.delete('aec'+i+'.pcm' )     
                    fp.close()                    
    
                    strFileCapName =  path_ftp  +  '\\cap'+i+'.pcm'                
                    fp = open(strFileCapName,'wb')     
                    ftp.rename('cap.pcm', 'cap'+i+'.pcm')
                    ftp.retrbinary('RETR ''cap'+i+'.pcm''', fp.write, bufsize)  
                    ftp.delete('cap'+i+'.pcm')     
                    fp.close() 
    
                    strFileRefName =  path_ftp  +  '\\ref'+i+'.pcm'                
                    fp = open(strFileRefName,'wb')    
                    ftp.rename('ref.pcm', 'ref'+i+'.pcm' ) 
                    ftp.retrbinary('RETR ''ref'+i+'.pcm''', fp.write, bufsize)  
                    ftp.delete('ref'+i+'.pcm')     
                    fp.close() 	
    
                    i=int(i)
                    i=i+1
                #--------------------------aec结果自动化判断工具----------------------#
                    strcmdftp ='D:\\AEC_Auto_test\\AECResultAutoAnalysis.exe '+strFileAecName+' 48000 -60 ' +ref +' -6 '+mode
                    print strcmdftp
                    subprocess.call(strcmdftp)
                #-------------------------对结果进行判断进入不同结果的文件夹-------------------------#
                    f = codecs.open('C:\\Users\\Administrator\\Desktop\\AECResultAutoAnalysisLog.csv','r','gbk')
                    s = f.readlines()
                    f.close()
                    for line in s:
                        csvfile = line.encode('gbk')
                    csvfile=re.split(',',csvfile)
                    print csvfile[3]
                    shutil.move(path_ftp,"D:\\AEC_Auto_test\\test_result\\"+csvfile[3])
                    sched_Timer = sched_Timer+datetime.timedelta(seconds=120)
        #-------------------------循环结束后删除空白文件夹-------------------------#  
            def del_emfile(path = "D:\\AEC_Auto_test\\test_result\\"):
                folder_num = 0
                efile = []
                for i in os.walk(path):
                    if len( i[1] ) == 0 and len( i[2] ) == 0:
                        efile.append( i[0] )
                        os.rmdir(i[0])  
                        folder_num +=1 
                if __name__ == '__main__':
                    d = del_emfile()   
            ftp.quit()
            ftp.close()              
        #-------------------------时间设定模块-------------------------# 
        Y = int(time.strftime('%Y'))
        m = int(time.strftime('%m'))
        d = int(time.strftime('%d'))   
        sched_Timer = datetime.datetime(Y,m,d,H,M,S,MS)
        if mode=='s':
            os.mkdir("D:\\AEC_Auto_test\\test_result\\F" )
            os.mkdir("D:\\AEC_Auto_test\\test_result\\P" )
        else:
            os.mkdir("D:\\AEC_Auto_test\\test_result\\P" )
            os.mkdir("D:\\AEC_Auto_test\\test_result\\"+u"有压制" )
            os.mkdir("D:\\AEC_Auto_test\\test_result\\"+u"待人工检查" )
            #os.mkdir("F:\\AEC_Auto_test\\test_result\\F" )
    
        print 'run the timer task at {0}'.format(sched_Timer)
        timerFun(sched_Timer)  
    else:
        #-------------------------外厂商终端-------------------------#
        def timerFun(sched_Timer): 
            i = 1
            while True:
                #-------------------------创建文件夹-------------------------#
                path_cap = "D:\\AEC_Auto_test\\test_result\\" + time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
                #print path_cap
                os.mkdir(path_cap)
                i=str(i)
                strFileCapAecName = path_cap +  '\\aec'+i+'.pcm' 
                i= int(i)
                i = i+1                
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
                if  datetime.datetime.now() >= sched_Timer :		
                    print datetime.datetime.now()
                    print "wave_PLAY()"
                    #-------------------------采集音频-------------------------#
                    strcmdcap1 = 'D:\\AEC_Auto_test\\ffmpeg -f dshow -i audio=' + "\\aud_device\\"+ ' -f s16le -acodec pcm_s16le -ar 48000 -ac 1 -aframes 3000 '+ strFileCapAecName
                    subprocess.call(strcmdcap1)
                    #-------------------------播放音频-------------------------#  
                    #time.sleep(2)
                    wave_PLAY()
                    time.sleep(40)
                    #-------------------------aec结果自动化判断工具-------------------------# 
                    strcmdcap2 = 'D:\\AEC_Auto_test\\AECResultAutoAnalysis.exe '+strFileCapPcmName+' 48000 -60 '+ ref +' -6 '+mode
                    subprocess.call(strcmdcap2)
                    f = codecs.open('C:\\Users\\Administrator\\Desktop\\AECResultAutoAnalysisLog.csv','r','gbk')
                    s = f.readlines()
                    f.close()
                    for line in s:
                        csvfile = line.encode('gbk')
                    csvfile=re.split(',',csvfile)
                    print csvfile[3]
                    shutil.move(path_ftp,"D:\\AEC_Auto_test\\test_result\\"+csvfile[3])
                    sched_Timer = sched_Timer+datetime.timedelta(seconds=120)
                    
#-------------------------循环结束后删除空白文件夹-------------------------#                       
            def del_emfile(path = "D:\\AEC_Auto_test\\test_result\\"):
                folder_num = 0
                efile = []
                for i in os.walk(path):
                    if len( i[1] ) == 0 and len( i[2] ) == 0:
                        efile.append( i[0] )
                        os.rmdir(i[0])  
                        folder_num +=1 
            if __name__ == '__main__':
                d = del_emfile()   
            
            ftp.quit()
            ftp.close()                
    #-------------------------时间设定模块-------------------------# 
            Y = int(time.strftime('%Y'))
            m = int(time.strftime('%m'))
            d = int(time.strftime('%d'))   
            sched_Timer = datetime.datetime(Y,m,d,H,M,S,MS)
            if mode=='s':
                os.mkdir("D:\\AEC_Auto_test\\test_result\\F" )
                os.mkdir("D:\\AEC_Auto_test\\test_result\\P" )
            else:
                os.mkdir("D:\\AEC_Auto_test\\test_result\\P" )
                os.mkdir("D:\\AEC_Auto_test\\test_result\\"+u"有压制" )
                os.mkdir("D:\\AEC_Auto_test\\test_result\\"+u"待人工检查" )
                #os.mkdir("F:\\AEC_Auto_test\\test_result\\F" )
    
            print 'run the timer task at {0}'.format(sched_Timer)
            timerFun(sched_Timer)  
            
   
   
  
     



