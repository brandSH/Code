
import datetime
import sys  
import winsound  
import time, datetime
import datetime
import pyaudio
import wave
def wave_PLAY():
#�������������С
    chunk = 1024
#��.wav��ʽ�ļ�
    f = wave.open(r"C:\Users\wangyichao\Desktop\danjiang.wav","rb")
#ʵ����PyAudio
    p = pyaudio.PyAudio()
#��������
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                 channels = f.getnchannels(),
     rate = f.getframerate(),
     output = True)
#��ȡ����
    data = f.readframes(chunk)
#��������
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
#��Ƶ����
                wave_PLAY()
                print datetime.datetime.now()
#ָ��ѭ��ʱ��
                sched_Timer = sched_Timer+datetime.timedelta(seconds=120)
#ָ������ʱ��
sched_Timer = datetime.datetime(2017,8,16,10,43,0,100000)
print 'run the timer task at {0}'.format(sched_Timer)
timerFun(sched_Timer)