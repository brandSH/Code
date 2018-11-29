# -*- coding: cp936 -*-
from __future__ import division
import cv2
import numpy as np
import os
import sys
import time
from numpy import *
from time import ctime,sleep

#获得感知哈希表
def phash(cur_gray):
    #cur_gray=cv2.imread(imgfile, 0)
    # 缩小至32*32
    m_img = cv2.resize(cur_gray, dsize=(32, 32))
    # 浮点型用于计算
    m_img = np.float32(m_img)
    # 离散余弦变换，得到dct系数矩阵
    img_dct = cv2.dct(m_img)
    #img_dct.dump("DCT.txt")
    img_mean = cv2.mean(img_dct[0:8, 0:8])
    # 返回一个8*8bool矩阵
    return img_dct[0:8, 0:8] > img_mean[0]

#计算海明距离
def hammingDist(s1, s2):
    assert len(s1) == len(s2)   #assert断言是声明其布尔值必须为真的判定，如果发生异常就说明表达示为假。
    diff = np.uint8(s1 - s2)
    return cv2.countNonZero(diff)

#计算基于感知哈希表的相似度
def SimilarityPH(RefYUV,width1,height1,CookYUV,width2,height2):
    #读取YUV
    YUVr=open(RefYUV,'rb')
    OneFrmSize1=width1*height1*3/2 #yuv420
    YUVc=open(CookYUV,'rb')
    OneFrmSize2=width2*height2*3/2 #yuv420
    FrmCount=int(os.path.getsize(RefYUV)//OneFrmSize1)
    #FrmCount2=int(os.path.getsize(CookYUV)//OneFrmSize2)

    #创建结果输出文档
    TimeNow=time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))
    ResultFileName='SimilarityPH_Result_'+ str(RefYUV) + "_" + str(CookYUV) + "_" + TimeNow +'.txt'
    ResultFile=open(ResultFileName,'w')
    ResultFile.write('YUV: '+ str(RefYUV) + "," + str(CookYUV) +'\n'+'Frame Count: '+str(FrmCount)+'\n'+'Frame_No., Similarity_pHash')
    ResultFile.close()
    #print 'Start: '+ctime()
    #对每一帧进行计算
    Yr=[]    #创建存储Y的空矩阵
    Yc=[]
    for i in range(FrmCount):
        #读取帧并获取CannyImage
        YUVr.seek(OneFrmSize1*i,0)    #将文件指针指向帧开始
        YUVc.seek(OneFrmSize2*i,0)
        YrStrList = list(YUVr.read(width1 * height1))   #读取一帧并转为列表，每一个Y值对应一个元素，属性为字符串。
        YcStrList = list(YUVc.read(width2 * height2))
        YrList = map(ord, YrStrList)  #使用map将list里每一个字符串转换为字符串所对应ASCII码
        YcList = map(ord, YcStrList)
        Yr = np.array(YrList).reshape(height1,width1)   #将列表转为矩阵
        Yc = np.array(YcList).reshape(height2,width2)
        cv2.imwrite("r.bmp",Yr)
        cv2.imwrite("c.bmp",Yc)
        GrayImageR = cv2.imread("r.bmp",0)     #若直接使用Y，OpenCV会报错
        GrayImageC = cv2.imread("c.bmp",0)
         #由于可能出现YUV.bmp未生成就被使用的情况，因此当GrayImage为“NoneType”类型时再次读取
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