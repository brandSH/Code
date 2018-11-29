# -*- coding: cp936 -*-
#使用单pool获得返回值
#通过多进程写文件而不是获得进程返回值的方式实现了进程的并行处理，优化了速度，1080P大概减少了3~4s
#实现了测试结果的文件输出
#使用方法：EPSNR.py RefYUVName CookedYUVName width height
#注意：YUV文件要放在和EPSNR同级目录下
import cv2
import numpy as np
import math
import os
import sys
import threading
from numpy import *
from threading import Thread
from time import ctime,sleep
import time
import multiprocessing
from multiprocessing import Process

def EPSNR(EdgeImg,RefImg,CookedImg,height,width,ResultFileName,FrmNO):
    K = 0
    MSEedgeSum = 0.0 
    MSEedge = 0.0
    EPSNR = 0
    p = 0
    ResultFile=open(ResultFileName,'a')
    for i in range(0,height):
        for ii in range(0,width):
            if EdgeImg[i,ii]  > 0:
                RefValue = int(RefImg[i,ii])                           
                CookedValue = int(CookedImg[i,ii])               
                K= K +1
                MSEedgeSum = MSEedgeSum+(RefValue-CookedValue)**2 
            if p < RefImg[i,ii]:
                p = RefImg[i,ii]
    if MSEedgeSum == 0 :
        ResultFile.write('\n'+str(FrmNO)+' 100')
        ResultFile.close()
    else :
        MSEedge = MSEedgeSum / K
        EPSNR = (math.log10(p**2/MSEedge)) * 10
        ResultFile.write('\n'+str(FrmNO)+' '+str(EPSNR))
        ResultFile.close()

if __name__ == "__main__":        
    #screenLevels = 255.0     
    RefYUVPath=sys.argv[1]
    CookedYUVPath=sys.argv[2]
    width=int(sys.argv[3]) 
    height=int(sys.argv[4])
    RefYUVFile=open(RefYUVPath,'rb')
    CookedYUVFile=open(CookedYUVPath,'rb')
    OneFrmSize=width*height*3/2 #yuv420
    FrmCount=os.path.getsize(RefYUVPath)/OneFrmSize
    TimeNow=time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
    sobelXResultFileName='SobelXResult_'+CookedYUVPath+TimeNow+'.txt'
    sobelYResultFileName='SobelYResult_'+CookedYUVPath+TimeNow+'.txt'
    sobelXResultFile=open(sobelXResultFileName,'w')
    sobelXResultFile.write('Ref: '+RefYUVPath+'\n'+'Cooked: '+CookedYUVPath+'\n'+'Frame Count: '+str(FrmCount)+'\n'+'Frame_No. EPSNR_sobelx')
    sobelYResultFile=open(sobelYResultFileName,'w')
    sobelYResultFile.write('Ref: '+RefYUVPath+'\n'+'Cooked: '+CookedYUVPath+'\n'+'Frame Count: '+str(FrmCount)+'\n'+'Frame_No. EPSNR_sobely')
    sobelXResultFile.close()
    sobelYResultFile.close()
    YRef=[]
    YReft=zeros((height,width),uint8,'C')
    YCooked=[]
    YCookedt=zeros((height,width),uint8,'C')
    for i in range(FrmCount):
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'Start: '+ctime()
        RefYUVFile.seek(OneFrmSize*i,0)
        CookedYUVFile.seek(OneFrmSize*i,0)
        for m in range(height):
            for n in range(width):
                YReft[m,n]=ord(RefYUVFile.read(1))
                YCookedt[m,n]=ord(CookedYUVFile.read(1))
        YRef=YRef+[YReft]
        YCooked=YCooked+[YCookedt]
        RefImg = YRef[0]
        CookedImg = YCooked[0]
        #print ctime(),'YRead'
        sobelx = cv2.Sobel(RefImg,cv2.CV_8U,1,0,ksize=5)
        sobely = cv2.Sobel(RefImg,cv2.CV_8U,0,1,ksize=5)

        #cv2.imwrite("cooked_%04d.png"%(i+1),CookedImg)
        #cv2.imwrite("ref_%04d.png"%(i+1),RefImg)
        #cv2.imwrite("sobelx_%04d.png"%(i+1),sobelx)
        #cv2.imwrite("sobely_%04d.png"%(i+1),sobely)
        #print ctime(),'Sobel'

        
        p1=multiprocessing.Process(target=EPSNR,args=(sobelx, RefImg, CookedImg, height, width,sobelXResultFileName,i+1))
        #print ctime(),'resultx'
        p2=multiprocessing.Process(target=EPSNR,args=(sobely, RefImg, CookedImg, height, width,sobelYResultFileName,i+1))
        #print ctime(),'resulty'
        p1.deamon=True
        p1.start()
        p2.deamon=True
        p2.start()
        p1.join()
        p2.join()
        #print ctime(),'pooly.join()'
        
        #Sprint i+1,' ',resultx,' ',resulty 
        print 'End: '+ctime()
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        
    RefYUVFile.close()
    CookedYUVFile.close()

    print 'Please press the enter key to exit!'
    raw_input()

