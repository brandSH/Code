
import datetime
import sys  
import winsound  
import time, datetime
import datetime
import pyaudio
import wave
def wave_PLAY():
#定义数据流块大小
    chunk = 1024
#打开.wav格式文件
    f = wave.open(r"C:\Users\wangyichao\Desktop\danjiang.wav","rb")
#实例化PyAudio
    p = pyaudio.PyAudio()
#打开数据流
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                 channels = f.getnchannels(),
     rate = f.getframerate(),
     output = True)
#读取数据
    data = f.readframes(chunk)
#播放数流
    while data != '':
        stream.write(data)
        data = f.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()
def timerFun(sched_Timer):    
    while True:
        now=datetime.datetime.now()
        exe = sched_Timer - now 
        a = exe.microseconds
        b = exe.seconds
        c = a/1000+b*1000
        d = c/1000
        if d>=2:
            time.sleep(1)
        else :
            time.sleep(0.001)
            
        if  datetime.datetime.now() >= sched_Timer :
                print datetime.datetime.now()
#音频播放
                wave_PLAY()
                print datetime.datetime.now()
#指定循环时间
                sched_Timer = sched_Timer+datetime.timedelta(seconds=120)
#指定播放时间
sched_Timer = datetime.datetime(2017,8,16,10,43,0,100000)
print 'run the timer task at {0}'.format(sched_Timer)
timerFun(sched_Timer)