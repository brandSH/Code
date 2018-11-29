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
    #height = EdgeImg.shape[0]   #����ÿά�Ĵ�С
    K = 0
    ImgList = EdgeImg.tolist()  #����ת�б�
    for i in range(height):
        K = K + ImgList[i].count(255)
    EdgeRate = K / EdgeImg.size
    return (K,EdgeRate)

#����YUVÿһ֡��������
def YUVEdgeRate(YUVFilePath,width,height):
    #��ȡYUV
    YUVFile=open(YUVFilePath,'rb')
    OneFrmSize=width*height*3/2 #yuv420
    FrmCount=int(os.path.getsize(YUVFilePath)//OneFrmSize)
    #�����������ĵ�
    TimeNow=time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
    ResultFileName='Result_'+YUVFilePath+TimeNow+'.txt'
    ResultFile=open(ResultFileName,'w')
    ResultFile.write('YUV: '+YUVFilePath+'\n'+'Frame Count: '+str(FrmCount)+'\n'+'Frame_No., EdgePixelCount, YUVEdgeRate')
    ResultFile.close()
    #print 'Start: '+ctime()
    #��ÿһ֡���м���
    Y=[]    #�����洢Y�Ŀվ���
    for i in range(FrmCount):
        #��ȡ֡����ȡCannyImage
        YUVFile.seek(OneFrmSize*i,0)    #���ļ�ָ��ָ��֡��ʼ
        YStrList = list(YUVFile.read(width * height))   #��ȡһ֡��תΪ�б�ÿһ��Yֵ��Ӧһ��Ԫ�أ�����Ϊ�ַ�����
        YList = map(ord, YStrList)  #ʹ��map��list��ÿһ���ַ���ת��Ϊ�ַ�������ӦASCII��    
        Y = np.array(YList).reshape(height,width)   #���б�תΪ����
        cv2.imwrite("YUV.bmp",Y)
        GrayImage = cv2.imread("YUV.bmp",0)     #��ֱ��ʹ��Y��OpenCV�ᱨ��
        #���ڿ��ܳ���YUV.bmpδ���ɾͱ�ʹ�õ��������˵�GrayImageΪ��NoneType������ʱ�ٴζ�ȡ
        while(type(GrayImage)=="NoneType"):
            GrayImage = cv2.imread("YUV.bmp",0)
        CannyImage = cv2.Canny(GrayImage,0,260)              
        #print 'End: '+ctime()
        
        #����������
        Result = GetEdgeRate(CannyImage,height)
        ResultFile=open(ResultFileName,'a')
        ResultFile.write('\n'+str(i)+', '+str(Result[0]) + ', ' + str(Result[1]))
        ResultFile.close()
        
        print str(i) + " frame complete!"

    YUVFile.close()

if __name__ == "__main__": 
    YUVFilePath = "XMPU_264_2M_2vmp_dec.yuv"
    YUVEdgeRate(YUVFilePath, 1920, 1080)