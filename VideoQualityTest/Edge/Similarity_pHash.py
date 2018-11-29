# -*- coding: cp936 -*-
from __future__ import division
import cv2
import numpy as np
import os
import sys
import time
from numpy import *
from time import ctime,sleep

#��ø�֪��ϣ��
def phash(cur_gray):
    #cur_gray=cv2.imread(imgfile, 0)
    # ��С��32*32
    m_img = cv2.resize(cur_gray, dsize=(32, 32))
    # ���������ڼ���
    m_img = np.float32(m_img)
    # ��ɢ���ұ任���õ�dctϵ������
    img_dct = cv2.dct(m_img)
    #img_dct.dump("DCT.txt")
    img_mean = cv2.mean(img_dct[0:8, 0:8])
    # ����һ��8*8bool����
    return img_dct[0:8, 0:8] > img_mean[0]

#���㺣������
def hammingDist(s1, s2):
    assert len(s1) == len(s2)   #assert�����������䲼��ֵ����Ϊ����ж�����������쳣��˵�����ʾΪ�١�
    diff = np.uint8(s1 - s2)
    return cv2.countNonZero(diff)

#������ڸ�֪��ϣ������ƶ�
def SimilarityPH(RefYUV,width1,height1,CookYUV,width2,height2):
    #��ȡYUV
    YUVr=open(RefYUV,'rb')
    OneFrmSize1=width1*height1*3/2 #yuv420
    YUVc=open(CookYUV,'rb')
    OneFrmSize2=width2*height2*3/2 #yuv420
    FrmCount=int(os.path.getsize(RefYUV)//OneFrmSize1)
    #FrmCount2=int(os.path.getsize(CookYUV)//OneFrmSize2)

    #�����������ĵ�
    TimeNow=time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
    ResultFileName='SimilarityPH_Result_'+ str(RefYUV) + "_" + str(CookYUV) + "_" + TimeNow +'.txt'
    ResultFile=open(ResultFileName,'w')
    ResultFile.write('YUV: '+ str(RefYUV) + "," + str(CookYUV) +'\n'+'Frame Count: '+str(FrmCount)+'\n'+'Frame_No., Similarity_pHash')
    ResultFile.close()
    #print 'Start: '+ctime()
    #��ÿһ֡���м���
    Yr=[]    #�����洢Y�Ŀվ���
    Yc=[]
    for i in range(FrmCount):
        #��ȡ֡����ȡCannyImage
        YUVr.seek(OneFrmSize1*i,0)    #���ļ�ָ��ָ��֡��ʼ
        YUVc.seek(OneFrmSize2*i,0)
        YrStrList = list(YUVr.read(width1 * height1))   #��ȡһ֡��תΪ�б�ÿһ��Yֵ��Ӧһ��Ԫ�أ�����Ϊ�ַ�����
        YcStrList = list(YUVc.read(width2 * height2))
        YrList = map(ord, YrStrList)  #ʹ��map��list��ÿһ���ַ���ת��Ϊ�ַ�������ӦASCII��
        YcList = map(ord, YcStrList)
        Yr = np.array(YrList).reshape(height1,width1)   #���б�תΪ����
        Yc = np.array(YcList).reshape(height2,width2)
        cv2.imwrite("r.bmp",Yr)
        cv2.imwrite("c.bmp",Yc)
        GrayImageR = cv2.imread("r.bmp",0)     #��ֱ��ʹ��Y��OpenCV�ᱨ��
        GrayImageC = cv2.imread("c.bmp",0)
         #���ڿ��ܳ���YUV.bmpδ���ɾͱ�ʹ�õ��������˵�GrayImageΪ��NoneType������ʱ�ٴζ�ȡ
        while(type(GrayImageR)=="NoneType"):
            GrayImageR = cv2.imread("r.bmp",0)
        while(type(GrayImageC)=="NoneType"):
            GrayImageC = cv2.imread("c.bmp",0)
        CannyImageR = cv2.Canny(GrayImageR,0,260)
        CannyImageC = cv2.Canny(GrayImageC,0,260)
        #print 'End: '+ctime()

        RpHash=phash(GrayImageR)
        CpHash=phash(GrayImageC)
        #Diff = hammingDist(RpHash,CpHash)
        similarity = 1 - hammingDist(RpHash,CpHash)*1. / 64

        ResultFile=open(ResultFileName,'a')
        ResultFile.write('\n'+str(i)+', '+str(similarity))
        ResultFile.close()

        print str(i) + " frame complete!"

    YUVr.close()
    YUVc.close()

if __name__ == "__main__":
    SimilarityPH("XMPU_264.yuv",1280,720,"XMPU5_264.yuv",1280,720)