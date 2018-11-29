# -*- coding: utf-8-*-
import re
import sys
import time 
import subprocess
import ftplib
import telnetlib
import datetime
import os
reload(sys)
sys.setdefaultencoding('utf-8')
#ftp取离线数据包

def ftp_download(srcIp,username1,password1,i,exe):
    time.sleep(1) 
    f = ftplib.FTP(srcIp)  
    f.login(username1, password1)  
    pwd_path = f.pwd()

    file_remote = 'data/local/tmp/body_video.data'
    file_remote1 = 'data/local/tmp/body_video.txt'
    #file_remote2 = 'data/local/tmp/cap.yuv'
    pwd = os.getcwd()
    now_time = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
    try:
        os.makedirs(pwd+'\\'+'high_light')
    except:
        pass
    try:
        os.makedirs(pwd+'\\'+'low_light')
    except:
        pass 
    path1 = pwd+'\\'+now_time
    os.makedirs(path1 )
    file_local = path1+'\\2.data'
    file_local1 = path1+'\\2.txt'
    #file_local2 = path1+'\\2.yuv' 
    bufsize = 1024
    try:
        fp = open(file_local, 'wb')
        
        f.retrbinary('RETR %s' % file_remote, fp.write, bufsize)
        fp = open(file_local1, 'wb')
        f.retrbinary('RETR %s' % file_remote1, fp.write, bufsize)
    #fp = open(file_local2, 'wb')
    #f.retrbinary('RETR %s' % file_remote2, fp.write, bufsize)    
        fp.close()
    except:
        pass 
    if exe == 0:
        command = 'ffmpeg.exe -r 60 -i  '+file_local+'  -vcodec copy  '+pwd+'\\'+'high_light\\'+now_time+'_body.mp4'
        print command
    else :
        command = 'ffmpeg.exe -r 60 -i   '+file_local+'   -vcodec copy  '+pwd+'\\'+'low_light\\'+now_time+'_body.mp4'
    subprocess.call(command)
    
#ftp中删除文件
def ftp_delete(srcIp,username1,password1,i):
    time.sleep(1) 
    f = ftplib.FTP(srcIp)  
    f.login(username1, password1)  
    pwd_path = f.pwd()

    file_remote = 'data/local/tmp/Dec[0]1920x1080RevStream_106.data'
    file_remote1 = 'data/local/tmp/Dec[0]1920x1080RevStream_106.data.txt'
    #file_remote2 = 'data/local/tmp/cap.yuv'
    toname = 'data/local/tmp/body_video.data'
    toname1 = 'data/local/tmp/body_video.txt'         
    try:
        f.delete(file_remote)
        f.delete(file_remote1)  
    except:
        pass
    try:
        f.delete(toname)
        f.delete(toname1)    
    except:
        pass
#判断ftp中是否存在
def ftp_alive(srcIp,username1,password1,i):
    time.sleep(1) 
    f = ftplib.FTP(srcIp)  
    f.login(username1, password1)  
    pwd_path = f.pwd()
    alive = 1

    file_remote = 'data/local/tmp/Dec[0]1920x1080RevStream_106.data'
    file_remote1 = 'data/local/tmp/Dec[0]1920x1080RevStream_106.data.txt'
    #file_remote2 = 'data/local/tmp/cap.yuv'
    toname = 'data/local/tmp/body_video.data'
    toname1 = 'data/local/tmp/body_video.txt'
    bufsize = 1024
    try:
        f.rename(file_remote, toname)
        f.rename(file_remote1, toname1)
    except:
        alive = 0
    return alive
#telnet 输入命令
def do_telnet(ip, port, user, password, commands):
    tn = telnetlib.Telnet(ip, port)
    tn.set_debuglevel(2)

    tn.read_until("Username:")
    tn.write(user + "\r\n")

    tn.read_until("Password:")
    tn.write(password + "\r\n")

    for command in commands:
        tn.write("\r\n")
        tn.write("\r\n")        
        tn.write(command + "\r\n")
        tn.write("\r\n")
        tn.write("\r\n")         

    
srcIp = '172.16.184.77'
port = 2501
username='admin'
password='admin'
username1 = 'root'
password1 = 'videodrvDZT888' 
commands=['savevdec 0 36000']
i=1

while 1:
    now=datetime.datetime.now()
    time.sleep(2)
    a=time.localtime()
    d = time.strftime("%w",a)                                   
    d_list = [1,2,3,4,5]
    if int(d) in d_list:
        c = 1
    else:
        c = 0
    print c
    if  ((now.hour >= 9 and now.hour<=11) or (now.hour >= 13 and now.hour<=21)) and c==1:  
        if now.hour >= 11 and now.hour<=13:
            exe = 1
        else:
            exe = 0
        try:
            ftp_delete(srcIp, username1, password1, i)
            time.sleep(10)
            do_telnet(srcIp, port, username, password, commands)
            time.sleep(120)
            alive = ftp_alive(srcIp,username1,password1,i)
            print 'alive================'+str(alive)
            if alive == 1:
                time.sleep(720)
            else:
                while 1:
                    print 'telnet 11111111111111'
                    do_telnet(srcIp, port, username, password, commands)
                    print 'telnet 22222222222222'
                    time.sleep(120)
                    alive = ftp_alive(srcIp,username1,password1,i)
                    print 'alive11================'+str(alive)
                    if alive== 1:
                        time.sleep(720)
                        break
                    else :
                        pass
            print '开始下载中..............'
            ftp_download(srcIp,username1,password1,i,exe)
            time.sleep(120)
            i=i+1
        except:
            print '请检查网络'
            pass
 
    else:
        print u'等待开始'