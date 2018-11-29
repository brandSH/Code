# -*- coding: cp936 -*-
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
import wave
import shutil
import subprocess

def Get_ref_file(path_ref_file):
	i=0
	ref=[]
	for root, dirs, files in os.walk(path_ref_file):
		for ref_name in files:
			#print (ref_name)
			ref.append(ref_name)
			i=i+1
	return ref

#ref_file = "maicong.wav"  
def wave_PLAY():
	chunk = 1024
	f = wave.open(r"C:\Users\Administrator\Desktop\X700-AEC\X700_shuangjiang_xing.wav","rb")
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
	
#NTP时间同步模块
def NTPTime(NTPServerIP):
	try:
		commandref="ntpdate -b " + NTPServerIP
		#subprocess.call(commandref)
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
	list.append(cf.getint("play","ISNTPServer"))
	list.append(cf.get("play","NTPServerIP"))
	return list

def timerFun(cycle_num,sched_Timer,play_interval,ISNTPServer,NTPServerIP): 
	ref=Get_ref_file(path_ref_file)
	NewCycle_Num=cycle_num*len(ref)
	i=0
	CapPath=os.getcwd() + "\\CapNoisePrejudge_Audio_file"
	while i<NewCycle_Num:
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
			#*-----------------时间同步模块----------------------*
			if ISNTPServer==0:
				if (i%30)==0:
					NTPTime(NTPServerIP)					
			#*-----------------新建文件夹--------------------------------*
			i=str(i) 
			path_ftp = CapPath + "\\" + time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
			os.mkdir(path_ftp )
			strFileCapAecName =  path_ftp  +  '\\capaec'+i+'.pcm' 								
			#*-----------------采集音频---------------------------------*
			strcmdcap1 = 'ffmpeg -f dshow -i audio=' + '\"线路输入 (Lexicon IO42 2.9.29)\"'+ ' -f s16le -acodec pcm_s16le -ar 48000 -ac 1 -t 45 '+ strFileCapAecName
			print strcmdcap1
			subprocess.call(strcmdcap1)
			#-------------------------延时循环播放-------------------------#
			sched_Timer = sched_Timer+datetime.timedelta(seconds=play_interval)
			
			i=int(i)
			i=i-1			

if __name__=="__main__":
	path_ref_file = os.getcwd() + "\\test_file\\"
	config_list=[]
	config_list=Get_config("config.ini")
	sched_Timer = datetime.datetime(config_list[1],config_list[2],config_list[3],config_list[4],config_list[5],config_list[6],100000)
	cycle_num=config_list[0]
	play_interval=config_list[7]
	ISNTPServer=config_list[8]
	NTPServerIP=config_list[9]
	print cycle_num,sched_Timer,play_interval,ISNTPServer,NTPServerIP
	timerFun(cycle_num,sched_Timer,play_interval,ISNTPServer,NTPServerIP)
