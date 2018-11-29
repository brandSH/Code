# -*- coding: cp936 -*-
from __future__ import division 
import cv2
import numpy as np
import os
import sys
import time
from numpy import *
from time import ctime,sleep

def GetEdgeRate(EdgeImg,height):
    #height = EdgeImg.shape[0]   #矩阵每维的大小
    K = 0
    ImgList = EdgeImg.tolist()  #矩阵转列表
    for i in range(height):
        K = K + ImgList[i].count(255)
    EdgeRate = K / EdgeImg.size
    return (K,EdgeRate)

#计算YUV每一帧的轮廓比
def YUVEdgeRate(YUVFilePath,width,height):
    #读取YUV
    YUVFile=open(YUVFilePath,'rb')
    OneFrmSize=width*height*3/2 #yuv420
    FrmCount=int(os.path.getsize(YUVFilePath)//OneFrmSize)
    #创建结果输出文档
    TimeNow=time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
    ResultFileName='Result_'+YUVFilePath+TimeNow+'.txt'
    ResultFile=open(ResultFileName,'w')
    ResultFile.write('YUV: '+YUVFilePath+'\n'+'Frame Count: '+str(FrmCount)+'\n'+'Frame_No., EdgePixelCount, YUVEdgeRate')
    ResultFile.close()
    #print 'Start: '+ctime()
    #对每一帧进行计算
    Y=[]    #创建存储Y的空矩阵
    for i in range(FrmCount):
        #读取帧并获取CannyImage
        YUVFile.seek(OneFrmSize*i,0)    #将文件指针指向帧开始
        YStrList = list(YUVFile.read(width * height))   #读取一帧并转为列表，每一个Y值对应一个元素，属性为字符串。
        YList = map(ord, YStrList)  #使用map将list里每一个字符串转换为字符串所对应ASCII码    
        Y = np.array(YList).reshape(height,width)   #将列表转为矩阵
        cv2.imwrite("YUV.bmp",Y)
        GrayImage = cv2.imread("YUV.bmp",0)     #若直接使用Y，OpenCV会报错
        #由于可能出现YUV.bmp未生成就被使用的情况，因此当GrayImage为“NoneType”类型时再次读取
        while(type(GrayImage)=="NoneType"):
            GrayImage = cv2.imread("YUV.bmp",0)
        CannyImage = cv2.Canny(GrayImage,0,260)              
        #print 'End: '+ctime()
        
        #计算轮廓比
        Result = GetEdgeRate(CannyImage,height)
        ResultFile=open(ResultFileName,'a')
        ResultFile.write('\n'+str(i)+', '+str(Result[0]) + ', ' + str(Result[1]))
        ResultFile.close()
        
        print str(i) + " frame complete!"

    YUVFile.close()

if __name__ == "__main__": 
    YUVFilePath = "XMPU_264_2M_2vmp_dec.yuv"
    YUVEdgeRate(YUVFilePath, 1920, 1080)