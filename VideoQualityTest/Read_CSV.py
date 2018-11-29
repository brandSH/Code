# coding=utf8

import csv
import numpy
import os 
import math



#---------------文件目录、测试序列、码率，需要填写---------------#    
FilePath = r'D:\1-zp\XMPU5_Video\New_XMPU5_H264_1080P-H265'
testfile = ["duoren"]
data = ["1M"]  

RowList=[]
NewRowList = [] 

for i in range(len(testfile)):

    for j in range(len(data)):
        
        CSV_Org_File = FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + ".csv"
        print CSV_Org_File
        
        txt_file =  FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "New_VQCResult_O_" + testfile[i] + "_" + data[j] + ".txt"
        print txt_file
        
        ftxt = open(txt_file,'w')  
        
        with open(CSV_Org_File) as csvfile:
            mLines = csvfile.readlines()
        
        if testfile[i] == "excel" or testfile[i] == "excel_60fps" or testfile[i] == "word" or testfile[i] == "ppt":
            targetLine = mLines[8]
        else :
            targetLine = mLines[12]
        
        #print targetLine
        
        RowList = targetLine.split(';')
        #print RowList           
        
        Avr = float(RowList[2])
        print "Average:"+str(Avr)
        
        del RowList[0:3]
        del RowList[-1]
        
        NewRowList = map(float,RowList)
        #print "NewRowList:" + str(NewRowList)
        
        Max = max(NewRowList)
        Min = min(NewRowList)
        
        print "Max:" + str(Max)
        print "Min:" + str(Min)
        
        sum1 = 0       
        for m in range(len(NewRowList)):     
            num = NewRowList[m]
            #print num
            numper = abs(float(num) - float(Avr))
            num2 = numper * numper
            sum1=sum1+num2
        n=len(NewRowList)
        STDEVP = math.sqrt((sum1/n))
        print "STDEVP:" + str(STDEVP)
        ftxt.write('Average:'+str(Avr)+'\n')
        ftxt.write('STDEVP:'+str(STDEVP)+'\n')
        ftxt.write('Max:'+str(Max)+'\n')
        ftxt.write('Min:'+str(Min)+'\n')        
        ftxt.close() 
            
            
      
                        
            
            




    
