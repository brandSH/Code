# -*- coding: utf-8-*-
import telnetlib_son
import subprocess
import os
import time
import sys
import pyshark
import threading			
import datetime
import codecs
import paramiko
import ftplib
import sys
import time 
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from winpcapy import WinPcapUtils
from winpcapy import WinPcapDevices
from winpcapy import WinPcap
from ctypes import *
from ctypes.util import find_library
import re
reload(sys)
sys.setdefaultencoding('utf-8')

#自动获取端口号
def send_video_port(ip, port, user, password,dstIp):
    tn = telnetlib_son.Telnet_print(ip, port)
    tn.set_debuglevel(1)
    tn.read_until("Username:")
    tn.write(user + "\r\n")
    tn.read_until("Password:")
    tn.write(password + "\r\n")  
    tn.write("\r\n")
    tn.write("\r\n")
    tn.write('mncl 1 1 1\r\n')
    port_print = tn._read_extra('mncl 1 1 1\r\n')
    send_port =  re.findall(r"Send\[(.+?)\] start=1 type=106",port_print)
    video_port =  re.findall(r"send rtp remote addr:    ip="+dstIp+", port=(.*)",port_print)
    return send_port,video_port

#自动获取medianet版本号
def medianet_version(ip, port, user, password):
    tn = telnetlib_son.Telnet_print(ip, port)
    tn.set_debuglevel(1)
    tn.read_until("Username:")
    tn.write(user + "\r\n")
    tn.read_until("Password:")
    tn.write(password + "\r\n")  
    tn.write("\r\n")
    tn.write("\r\n")
    tn.write('mnhelp\r\n')
    port_print = tn._read_extra('mnhelp\r\n')
    version = re.findall(r"time(.*)",port_print)
    return version
    
def recv_video_port(ip, port, user, password):
    tn = telnetlib_son.Telnet_print(ip, port)
    tn.set_debuglevel(1)
    tn.read_until("Username:")
    tn.write(user + "\r\n")
    tn.read_until("Password:")
    tn.write(password + "\r\n")  
    tn.write("\r\n")
    tn.write("\r\n")
    tn.write('mncl 1 1 1\r\n')
    port_print = tn._read_extra('mncl 1 1 1\r\n')
    recv_port =  re.findall(r"Recv\[(.+?)\] start=1 type=106",port_print)
    return recv_port

#根据打印判断视频是否卡顿
def video_fps_judge(ip, port, user, password,recv_port):
    tn = telnetlib_son.Telnet_print(ip, port)
    tn.set_debuglevel(1)
    tn.read_until("Username:")
    tn.write(user + "\r\n")
    tn.read_until("Password:")
    tn.write(password + "\r\n")  
    tn.write("\r\n")
    tn.write("\r\n")
    tn.write('mnhp '+str(recv_port[0])+' 4 3')
    tn.write("\r\n")
    tn.write("\r\n")    
    fps_print = tn._read_extra('mnhp '+str(recv_port[0])+' 4 3')
    misses =  re.findall(r"miss=1",fps_print)
    print fps_print
    print len(misses)
    return len(misses)
    

#发送端是否开启丢包重传
def send_command_retransmission(sendRetransmissionSwitch,send_port):
    if sendRetransmissionSwitch == 0:
        cmd_retransmission = 'mnar '+str(send_port[0])+' 0'
    else :
        cmd_retransmission = 'mnar '+str(send_port[0])+' 1'
    return cmd_retransmission

#接收端是否开启丢包重传
def  receive_command_retransmission(receiveRetransmissionSwitch,recv_port):
    if receiveRetransmissionSwitc
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    h == 0:
        cmd_retransmission = '0 '+str(recv_port[0])+' 0'
    else :
        cmd_retransmission = 'mnar '+str(recv_port[0])+' 1'
    return cmd_retransmission

#是否强制发送FEC包
def send_command_sendFec(sendFecSwitch,send_port):
    if sendFecSwitch == 1:
        cmd_sendFec = 'mnaf_send '+str(send_port[0])+' 1 5 25 0 100'
    else :
        cmd_sendFec = 'mnaf_fs 0'
    return cmd_sendFec  

#接收端是否开启FEC
def receive_command_openFec(receiveOpenFecSwitch,recv_port):
    if receiveOpenFecSwitch == 1:
        cmd_receiveOpenFec = 'mnaf '+str(recv_port[0])+' 1'
    else :
        cmd_receiveOpenFec = 'mnaf '+str(recv_port[0])+' 0'
    return cmd_receiveOpenFec  

#发送端是否开启FEC
def send_command_openFec(sendOpenFecSwitch,send_port):
    if sendOpenFecSwitch == 1:
        cmd_sendOpenFec = 'mnaf '+str(send_port[0])+' 1'
    else :
        cmd_sendOpenFec = 'mnaf '+str(send_port[0])+' 0'
    return cmd_sendOpenFec  

#发送丢包设置
def send_command_lose(sendloseRate,send_port):
    try:
        comd_send_lose = ' '.join(('mnsl '+str(send_port[0])+' 2',sendloseRate))
    except:
        print u'请检查视频源'
        sys.exit()
    return comd_send_lose  

#接收丢包设置
def receive_command_lose(receiveloseRate,recv_port):
    comd_receive_lose = ' '.join(('mnsl '+str(recv_port[0])+' 2',receiveloseRate))
    return comd_receive_lose   

def do_telnet(ip, port, user, password, commands):
    tn = telnetlib_son.Telnet_print(ip, port)
    tn.set_debuglevel(1)
    tn.read_until("Username:")
    tn.write(user + "\r\n")
    tn.read_until("Password:")
    tn.write(password + "\r\n")
    #tn.read_until(finish)
    for command in commands:
        tn.write("\r\n")
        tn.write("\r\n")
        time.sleep(2)
        tn.write(command + "\r\n")    
    tn.close()
    
#获取打印
def do_telnet_info(ip, port, user, password, commands):
    tn = telnetlib_son.Telnet_print(ip, port)
    tn.set_debuglevel(1)
    tn.read_until("Username:")
    tn.write(user + "\r\n")
    tn.read_until("Password:")
    tn.write(password + "\r\n")
    for command in commands:
        tn.write("\r\n")
        tn.write("\r\n")
        tn.write(command + "\r\n")    
        tn.wirte_info(command + "\r\n") 
    tn.close() 
    
#丢包率变化设置
def lose_rate_change(ip, port, user, password, commands):
    do_telnet(ip, port, user, password, commands)
    
def get_driver():
    driver= webdriver.Firefox()
    return driver

#登录web
def logon_web(driver,srcIp):
    driver.get("http://"+srcIp+"/") #终端 MTC 网站
    driver.find_element_by_id("loginAccount").send_keys("admin") #输入用户名
    driver.find_element_by_id("lpassword").send_keys("admin123") #输入密码
    driver.find_element_by_id("loginSubmit").click() #点击登录
    print (u"登录终端 Web 界面成功！")
    driver.implicitly_wait(30)
    #driver.switch_to_frame("contentFrame") #切换 frame
    
#呼叫会议
def call(rate,driver,dstIp):
    driver.switch_to_frame("contentFrame")
    try:
        WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'html body div.contentLeft div#accordion1.accordion div.accordion-group div#userSettings.accordion-body.in.collapse div.accordion-inner div.tab-kdv.tabActive div.tab-box-kdv form#callformid div.tabContent div#callinfoTwo.tabContent.left div.left input#callinfoOneId.inputText')))
        driver.find_element_by_css_selector("html body div.contentLeft div#accordion1.accordion div.accordion-group div#userSettings.accordion-body.in.collapse div.accordion-inner div.tab-kdv.tabActive div.tab-box-kdv form#callformid div.tabContent div#callinfoTwo.tabContent.left div.left input#callinfoOneId.inputText").send_keys(dstIp)
    except:
        print  111111111111111111
    try:
        WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div[2]/div/div[2]/div/form/div[1]/div[4]/div[1]/div[1]/input')))
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[2]/div/form/div[1]/div[4]/div[1]/div[1]/input").clear()
    except:
        print  222222222222222222    
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[2]/div/form/div[1]/div[4]/div[1]/div[1]/input").send_keys(int(rate)) # 填写码率
    try:
        WebDriverWait(driver, 20, 0.5).until(EC.element_to_be_clickable((By.ID,'callid')))
        driver.find_element_by_id("callid").click() #呼叫终端
    except:
        print  333333333333333333

#结束会议
def over_call(driver):  
    driver.switch_to_frame("contentFrame") #切换到结束会议表单中
    try:
        WebDriverWait(driver, 20, 0.5).until(EC.element_to_be_clickable((By.CLASS_NAME,'btnMain')))
        driver.find_element_by_class_name("btnMain").click() #点击“结束会议”按键
    except:
        print  44444444444444444444 
    driver.switch_to_default_content() #跳换到最外层界面
    try:
        WebDriverWait(driver, 20, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'html body div#alertid div.modal table tbody tr td div.modal-body div div.btnBox.btnBox28.confirm div.btn div.btnMain')))
        driver.find_element_by_css_selector('html body div#alertid div.modal table tbody tr td div.modal-body div div.btnBox.btnBox28.confirm div.btn div.btnMain').click()#点击“确认”按键
    except:
        driver.find_element_by_class_name("btnMain").click() #点击“结束会议”按键
        print  555555555555555555555
    print ("会议结束")
    
#ftp取离线数据包
def ftp_download(srcIp,username1,password1,rate,packet_name,delay_time):
    time.sleep(1) 
    f = ftplib.FTP(srcIp)  
    f.login(username1, password1)  
    pwd_path = f.pwd()
    file_remote = 'user/netcap/capfile/UsrNetCap0.pcap'
    file_local = u'D:\\wyc\\net_test_packet\\'+rate+'_'+packet_name+'_'+delay_time+'.pcap'
    bufsize = 1024  
    fp = open(file_local, 'wb')
    f.retrbinary('RETR %s' % file_remote, fp.write, bufsize)
    fp.close()
    
#保存数据包
def save_pcap(driver,rate,packet_name,delay_time):
    try:
        WebDriverWait(driver, 20, 0.5).until(EC.element_to_be_clickable((By.ID,'settingHref')))
        driver.find_element_by_id('settingHref').click()#点击设置
    except:
        print  6666666666666666666
    try:
        WebDriverWait(driver, 20, 0.5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[2]/ul/li[4]/a/span[2]')))    
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/ul/li[4]/a/span[2]').click()#点击扩展工具
    except:
        print  777777777777777777777 
        driver.find_element_by_id('settingHref').click()#点击设置
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/ul/li[2]/a/span[1]').click()#点击抓包工具
    time.sleep(5)
    driver.switch_to_frame('contentFrame')
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div/div/div[1]/div').click()#开始抓包
    time.sleep(10)#抓包时间
    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div/div/div[1]/div').click()#停止抓包
    time.sleep(5)
    ftp_download(srcIp,username1,password1,rate,packet_name,delay_time)#ftp中取数据包
    driver.implicitly_wait(30)
    driver.switch_to_default_content()
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/a[4]/span').click()#返回呼叫界面    
    
 #分析数据包   
def analyze_pcap(pcapfile,srcIp,video_port):
    e =0
    for media_port in video_port:
        print "udp.port=="+media_port+"&&ip.src=="+srcIp
        print 'udp.port=='+media_port
        cap = pyshark.FileCapture(pcapfile,display_filter="udp&&ip.src=="+srcIp,decode_as = {'udp.port=='+media_port:'rtp'})
        for cap1 in cap:
            try:
                fec_packet = cap1.rtp.p_type
                if int(fec_packet) == 124:  
                    e = e+1
                    break
            except:
                pass
    if e==0:
        start_fec = u'否'
        ftxt = open('info_hard.txt','a+')
        print_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        ftxt.write('\n++++++++++++++++++FEC未启动++++++++++++++++++'+print_time+'\n')
        ftxt.close()
    else:
        start_fec = u'是'
        ftxt = open('info_hard.txt','a+')
        print_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        ftxt.write('\n++++++++++++++++++FEC已启动++++++++++++++++++'+print_time+'\n')
        ftxt.close()
    return start_fec
        
 #通过WANem设置延时      
def delay_set(delay_time,srcIp,dstIp):
    wanEM_driver= webdriver.Firefox()
    wanEM_driver.get("http://172.16.178.163/WANem/") #终端 MTC 网站
    print 1
    wanEM_driver.implicitly_wait(30)
    wanEM_driver.switch_to_frame('WANEM_TITLE')
    wanEM_driver.find_element_by_xpath('/html/body/div/table/tbody/tr[2]/td/div/table/tbody/tr/td[4]').click()#网口选择界面
    time.sleep(5)
    wanEM_driver.switch_to_default_content()
    wanEM_driver.switch_to_frame('WANEM_MAIN')
    wanEM_driver.find_element_by_css_selector('html body div form table tbody tr td p b input').click()#选择网口进行设置
    wanEM_driver.find_element_by_xpath("/html/body/form[1]/center/div/table[1]/tbody/tr[4]/td[2]/input").clear()    
    wanEM_driver.find_element_by_xpath('/html/body/form[1]/center/div/table[1]/tbody/tr[4]/td[2]/input').send_keys(delay_time)#输入延时
    wanEM_driver.find_element_by_xpath("/html/body/form[1]/center/div/table[3]/tbody/tr/td[2]/input").clear()    
    wanEM_driver.find_element_by_xpath('/html/body/form[1]/center/div/table[3]/tbody/tr/td[2]/input').send_keys(srcIp) #输入发送端IP
    wanEM_driver.find_element_by_xpath("/html/body/form[1]/center/div/table[3]/tbody/tr/td[4]/input").clear()    
    wanEM_driver.find_element_by_xpath('/html/body/form[1]/center/div/table[3]/tbody/tr/td[4]/input').send_keys('255.255.255.255') 
    
    wanEM_driver.find_element_by_xpath("/html/body/form[1]/center/div/table[3]/tbody/tr/td[6]/input").clear()    
    wanEM_driver.find_element_by_xpath('/html/body/form[1]/center/div/table[3]/tbody/tr/td[6]/input').send_keys(dstIp) #输入发送端IP
    wanEM_driver.find_element_by_xpath("/html/body/form[1]/center/div/table[3]/tbody/tr/td[8]/input").clear()    
    wanEM_driver.find_element_by_xpath('/html/body/form[1]/center/div/table[3]/tbody/tr/td[8]/input').send_keys('255.255.255.255')     
    
    wanEM_driver.find_element_by_xpath('/html/body/form[1]/p/input[2]').click()
    
#写结果
def WriteTestResult(TestResultFileName,ResultHead,Result):    
    if os.path.exists(TestResultFileName) == False:
        TestResultFile = open(TestResultFileName,'w')
        TestResultFile.write(ResultHead+'\n'+Result)
    else: 
        TestResultFile = open(TestResultFileName,'a')
        TestResultFile.write('\n'+Result)                 
    TestResultFile.close()  

if __name__ == '__main__':
    
    
    
    #发送端及接收端IP
    srcIp='172.16.178.4'
    dstIp='172.16.178.170'    
    
    #FTP用户名密码
    username1 = 'root'
    password1 = 'videodrvDZT888'  
    
    #测试码率及测试延时的列表
    rate_list = ['1024','2048','4096'] 
    delay_time_list = ['0','200']

    #telnet端口号
    port1=2501
    port=2501
    
    #telnet用户名密码
    username='admin'
    password='admin'
    
    version=medianet_version(srcIp, port1, username, password)
    #输出表格头
    ResultHead = '版本日期：'+version[0]+u'\n会议延时,会议码率,丢包率,FEC是否启动,视频是否卡顿'
    finish='kdvmt->'
    #misses = video_fps_judge(dstIp, port, username, password,recv_port)
    #if misses == 0 :
        #print 11111
    #else:
        #print 22222
    #print misses
    global flag
    flag = 1
    for delay_time in delay_time_list:
        delay_set(delay_time,srcIp,dstIp)
        for rate in rate_list:
            #丢率设置
            receiveloseRate_list = ['0 0','2 2','5 2','10 2']
            for receiveloseRate in receiveloseRate_list:
                driver = get_driver()
                logon_web(driver,srcIp)        
                time.sleep(10)
                call(rate,driver,dstIp)  
                if flag == 1:
                    time.sleep(5)
                    send_port,video_port = send_video_port(srcIp, port1, username, password,dstIp)
                    recv_port = recv_video_port(dstIp, port, username, password)
                print recv_port,send_port
                flag = flag+1                
                ftxt = open('info_hard.txt','a+')
                ftxt.write(u'\n码率为：'+rate+'kbps\n')
                ftxt.write(u'\n丢包率为：'+receiveloseRate[0:2]+'%\n')
                ftxt.write(u'\n延时为：'+delay_time+'ms\n')
                ftxt.close()                         
                #发送端配置
                sendRetransmissionSwitch = 0
                sendFecSwitch = 0
                sendloseRate = '0 0'
                sendOpenFecSwitch = 1
                send_cmd=['setftp on','setptlevel 1','mnhu',send_command_lose(sendloseRate,send_port),send_command_retransmission(sendRetransmissionSwitch,send_port),send_command_sendFec(sendFecSwitch,send_port),send_command_openFec(sendOpenFecSwitch,send_port)]
                
                #接收端配置
                receiveRetransmissionSwitch = 0
                receiveOpenFecSwitch = 1
                receive_cmd=['setftp on','setptlevel 1','mnhu','mnsl '+str(recv_port[0])+' 2 0 0',receive_command_lose(receiveloseRate,recv_port),receive_command_retransmission(receiveRetransmissionSwitch,recv_port),receive_command_openFec(receiveOpenFecSwitch,recv_port)]
                
                #打印command
                info_conmmand = ['mnhr '+str(send_port[0])+' 8']
                send_commands=send_cmd
                resever_commands=receive_cmd
                
                #清除丢包率配置
                send_commands1=['mnsl '+str(send_port[0])+' 2 0 0']
                resever_commands1= ['mnsl '+str(recv_port[0])+' 2 0 0'] 
                
                do_telnet(srcIp, port1, username, password, send_commands)
                do_telnet(dstIp, port, username, password, resever_commands)
                do_telnet_info(srcIp, port1, username, password, info_conmmand)
                packet_name = receiveloseRate[0:2].replace(' ', '')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                save_pcap(driver,rate,packet_name,delay_time)#保存数据包
                pcapfile =u'D:\\wyc\\net_test_packet\\'+rate+'_'+packet_name+'_'+delay_time+'.pcap'
                open_fec_judge = analyze_pcap(pcapfile,srcIp,video_port) 
                
                #组帧分析
                misses = video_fps_judge(dstIp, port, username, password,recv_port)
                if misses == 0 :
                    video_effect=u'否'
                    ftxt = open('info_hard.txt','a+')
                    ftxt.write('\n++++++++++++++++++视频未卡顿+++++++++++++++++\n')
                    ftxt.close()
                else:
                    video_effect=u'是'
                    ftxt = open('info_hard.txt','a+')
                    ftxt.write('\n++++++++++++++++++视频卡顿+++++++++++++++++\n')
                    ftxt.close() 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                Result=','.join((delay_time,rate,receiveloseRate[0:2],open_fec_judge,video_effect))
                TestResultFileName = 'FECtest.csv' 
                WriteTestResult(TestResultFileName,ResultHead,Result)
                
                #清除丢包率
                do_telnet(srcIp, port1, username, password, send_commands1)
                do_telnet(dstIp, port, username, password, resever_commands1) 
                
                over_call(driver)#断会
                driver.quit()#关闭浏览器
        
