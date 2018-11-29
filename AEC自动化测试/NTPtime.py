# coding: utf-8
import os
import subprocess
import getpass,datetime
import time
import logging  

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='test.log',  
                    filemode='w')  
  
#logging.debug('debug message')  
#logging.info('info message')  
#logging.warning('warning message')  
#logging.error('error message')  
#logging.critical('critical message')  

def NTPTime():
    commandref="ntpdate -b 172.16.178.204"
    #subprocess.call(commandref)
    var = os.popen(commandref)
    NTPstr=var.read(500)
    #print NTPstr
    if NTPstr.index(" step time server 172.16.178.204 offset"):
        NTPstr=NTPstr.split()
        delytime=NTPstr[NTPstr.index('offset')+1]
        logging.info(delytime) 
        print delytime
        #print "sucess!"

def timerFun(sched_Timer):
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
                if  datetime.datetime.now() >= sched_Timer :		
                    print datetime.datetime.now()
                    logging.info(datetime.datetime.now()) 
                    if (i%30)==0:
                        NTPTime()
                    i=i+1
                    sched_Timer = sched_Timer+datetime.timedelta(seconds=60)

if __name__=='__main__':
    sched_Timer = datetime.datetime(2018,2,8,20,12,0,100000)
    cycle_num=1000
    timerFun(sched_Timer)
                                                                
                        


