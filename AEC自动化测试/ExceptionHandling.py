# -*- coding: UTF-8 -*-
#本模块功能是对可能出现问题的地方做异常处理，若出现问题则写入log日志文件，并注明造成异常的原因
#import Cap_AEC
import logging
import getpass,datetime
import time
import ConfigParser

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

#日志模块
logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='test.log',  
                    filemode='a') 

#因测试人员配置配置文件不规范造成的异常
def EH_Get_config():
        ConfigDict = Get_config("Config.ini")
        globals().update(ConfigDict)
        #对Sched_Timer配置项进行异常处理
        Sched_TimerFlag = 0
        try:
            NewSched_Timer = datetime.datetime.strptime(Sched_Timer, "%Y-%m-%d %H:%M:%S")
        except:
            Sched_TimerFlag = 1
            logging.error('Sched_Timer格式不规范！请从新配置Config.ini文件')
        if Sched_TimerFlag == 0:
            NewSched_Timer = datetime.datetime.strptime(Sched_Timer, "%Y-%m-%d %H:%M:%S")
            if datetime.datetime.now() >= NewSched_Timer:
                logging.critical('Sched_Timer程序开始时间小于当前时间！请从新配置Config.ini文件')
        #对Cycle_Num，Play_Interval，MinidB等int型配置项进行异常处理
        intlist = []
        intlist.append([Cycle_Num,Play_Interval,MinidB])
        for i in range(len(intlist[0])):
            try:
                int(intlist[0][i])
            except:
                logging.error('%s不是整数！请从新配置Config.ini文件' % intlist[0][i])
        #P对AECMod配置项进行异常处理
        if not AECMod.lower()=='s'or 'd':
            logging.error('AECMod配置有误！请从新配置Config.ini文件')


if __name__=='__main__':
        EH_Get_config()
        print "Test over! Please check  the test results!"