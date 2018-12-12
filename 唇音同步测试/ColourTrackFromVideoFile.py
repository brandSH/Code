#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ͨ��Ѱ����Ƶ�к�ɫ��������λ��ɫ���ֵ�ʱ��㣬�Թ����㴽��ͬ��ʱ��
#v1.0 2018-12-11 By ��չ
#��������ColourFind(videofile)��videofileΪ��Ƶ�ļ�·��
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np


#�ҳ�ÿһ�ο�ʼ�����ʱ��㣨��λ���룩
def ColourFind(videofile):
    cap = cv.VideoCapture(videofile)
    FPS = cap.get(5)
    
    frameID = 0
    RedFrame = []
    while(1):
        # Take each frame
        frameID = frameID + 1
        _, frame = cap.read()
        if frame is None:
            break
        # Convert BGR to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # define range of red color in HSV
        lower_red = np.array([0,43,46])
        upper_red = np.array([10,255,255])
        # Threshold the HSV image to get only blue colors
        mask = cv.inRange(hsv, lower_red, upper_red)
        # Bitwise-AND mask and original image
        res = cv.bitwise_and(frame,frame, mask= mask)
         
        height, width = mask.shape 
        areaMini = height * width * 0.3     #����ʵ��Ч�����е�����ɫ�����ռ��
        areas = []
        image, contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for ii in range(len(contours)):
            areas.append(cv.contourArea(contours[ii]))
        if len(areas) <> 0:        
            #print max(areas)
            if max(areas) > areaMini:
                #print frameID
                RedFrame.append(frameID)
                
        #resnew = cv.drawContours(res, contours, -1, (0,255,0), 3)#����������������
        #cv.imshow('resnew',resnew)
        #cv.imshow('frame',frame)
        #cv.imshow('mask',mask)
        #cv.imshow('res',res)
        #k = cv.waitKey(5) & 0xFF
    
    #print RedFrame
        
    #���ÿ������ĵ�һ֡ID
    Red = False
    FirstReds = []
    for i in range(1, len(RedFrame)):
        if RedFrame[i] - RedFrame[i-1] < 4 and Red == False:
            FirstReds.append(RedFrame[i-1]/FPS)
            Red = True       
        if RedFrame[i] - RedFrame[i-1] > 4:
            Red = False
    
    return FirstReds

    #����
if __name__ == "__main__": 
    videofile = 'VID_20181207_165610.mp4'
    print ColourFind(videofile)

    


