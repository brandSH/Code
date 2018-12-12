#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#通过寻找视频中红色区域来定位红色出现的时间点，以供计算唇音同步时差
#v1.0 2018-12-11 By 王展
#主函数：ColourFind(videofile)，videofile为视频文件路径
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np


#找出每一次开始闪红的时间点（单位：秒）
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
        areaMini = height * width * 0.3     #根据实际效果进行调整红色区域的占比
        areas = []
        image, contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for ii in range(len(contours)):
            areas.append(cv.contourArea(contours[ii]))
        if len(areas) <> 0:        
            #print max(areas)
            if max(areas) > areaMini:
                #print frameID
                RedFrame.append(frameID)
                
        #resnew = cv.drawContours(res, contours, -1, (0,255,0), 3)#把所有轮廓画出来
        #cv.imshow('resnew',resnew)
        #cv.imshow('frame',frame)
        #cv.imshow('mask',mask)
        #cv.imshow('res',res)
        #k = cv.waitKey(5) & 0xFF
    
    #print RedFrame
        
    #获得每次闪红的第一帧ID
    Red = False
    FirstReds = []
    for i in range(1, len(RedFrame)):
        if RedFrame[i] - RedFrame[i-1] < 4 and Red == False:
            FirstReds.append(RedFrame[i-1]/FPS)
            Red = True       
        if RedFrame[i] - RedFrame[i-1] > 4:
            Red = False
    
    return FirstReds

    #调试
if __name__ == "__main__": 
    videofile = 'VID_20181207_165610.mp4'
    print ColourFind(videofile)

    


