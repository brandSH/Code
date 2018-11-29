# -*- coding: UTF-8 -*-

import sys   
import os
import subprocess
import shutil
import csv
import re
import math
import time

#移动文件
def MoveFile(srcfile,dstfile):
                
    if not os.path.isfile(srcfile):
        print "%s not exist!"%(srcfile)
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
                os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        #print "move %s -> %s"%( srcfile,dstfile)
        
#获取当前路径
def fileDir() :
    path = sys.path[ 0 ]
    #print(path)
    #判断为脚本文件还是编译后文件，如果是脚本文件则返回脚本目录，否则返回编译后的文件路径
    if os.path.isdir( path ) :
        return path
    elif os.path.isfile( path ) :
        return os.path.dirname( path )

#获取文件后缀名
def suffix( file, *suffixName ) :
    array = map( file.endswith, suffixName )
    if True in array :
        return True
    else :
        return False

#删除目录下扩展名为.yuv .log的文件
def deleteFile() :
    targetDir = fileDir()
    for file in os.listdir( targetDir ) :
        targetFile = os.path.join( targetDir, file )
        if suffix( file, '.yuv', '.log'):
            os.remove( targetFile )
            
def text_save(filename, data):#filename为写入txt文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功") 
        
                

    
if __name__ == '__main__':
    
    testfile1 = ["duoren","danren","excel","word","ppt"]
    testfile2 = ["bag","ducks","park","pass","run","trailer","tree"]  
    
    testfileFrameCount1 = ["720","720","300","300","300"]
    testfileFrameCount2 = ["570","500","222","570","500","1253","500"]
    
    data1= ["8M","7M","6M","5M","4M","3M","2M","1M","768K","512K","256K"]
    
    #------文件目录、测试序列、码率、帧率，需要填写------#  
    FilePath = r'H:\ZP_File\ZP_XMPU5_Video'
    testfile =["duoren"]    
    data= ["3276K"]
    OrgFrame = 60
    
    avgFps = []
    File=[]
    
    for i in range(len(testfile)):
        
        for j in range(len(data)):
        
            dstfile = FilePath + "\\" + testfile[i] + "\\" + data[j]
           
            print dstfile  
            
            DataName = "enc1920x1080Hpayload_106.data"
           
            #--------------判断码流文件名--------------#            
            #if '1080P-H265' in FilePath :
                #if data[j] == "768K" or data[j] == "512K":
                    #DataName = "1280x720.emComTypeH265"                    
                #elif data[j] == "256K":
                    #DataName = "704x576.emComTypeH265"
                #else: 
                    #DataName = "1920x1080.emComTypeH265"               
                
            #elif '1080P-H264' in FilePath:
                #if data[j] == "768K" or data[j] == "512K":
                    #DataName = "1280x720.emComTypeH264"
                #elif data[j] == "256K":
                    #DataName = "704x576.emComTypeH264"
                #else: 
                    #DataName = "1920x1080.emComTypeH264"  
                
            #else: 
                #DataName = "3840x2160.emComTypeH265"
            
                    
            #---------------------------data转成YUV---------------------------#
            
            command_ffmpeg = "ffmpeg.exe -i "+ dstfile + "\\" + DataName + " -f rawvideo -pix_fmt yuv420p -video_size 1920x1080 " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv"
            print command_ffmpeg
            subprocess.call(command_ffmpeg)
            
            print "command_ffmpeg over!"
            
            
            #---------------------------imgalign对齐---------------------------#
            if testfile[i] == "duoren":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_1080P\\Video\\Marked_duoren_1920x1080_60fps_yuv420p.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_"+ data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign)
                
            elif testfile[i] == "duoren_30fps":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_1080P\\Video\\Marked_duoren_1920x1080_30fps_yuv420p.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + ".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign)                  
                
            elif testfile[i] == "danren":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_1080P\\Video\\Marked_danren_1920x1080_60fps-yuv420p.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign)
                
            elif testfile[i] == "excel_60fps":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_1080P\\SecondVideo\\Marked_Excel_1920x1080_60fps.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign) 
                
            elif testfile[i] == "excel_30fps":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_1080P\\SecondVideo\\Marked_Excel_1920x1080_30fps.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign)            
                
            elif testfile[i] == "word":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_1080P\\SecondVideo\\Marked_Word_1920x1080_30fps.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign)     
                
            elif testfile[i] == "ppt":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_1080P\\SecondVideo\\Marked_PPT_1920x1080_30fps.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign)    
                
            elif testfile[i] == "bag":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_other\\Marked_bag_1920x1080-420.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign)
                
            elif testfile[i] == "ducks":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_other\\Marked_ducks_1920x1080-420-50.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign)    
                
            elif testfile[i] == "park":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_other\\Marked_park_1080p50-short.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign) 
                
            elif testfile[i] == "pass":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_other\\Marked_pass_1080p-420p.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign)     
                
            elif testfile[i] == "run":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_other\\Marked_run_1920x1080-420-50.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign) 
                
            elif testfile[i] == "trailer":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_other\\Marked_trailer_2k-1080p24.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign) 
                
            elif testfile[i] == "tree":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_other\\Marked_tree_1080p50.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 1920 -h 1080"
                print command_imgalign
                subprocess.call(command_imgalign)
                
            elif testfile[i] == "4k_duoren":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_4K\\Marked_duoren_3840x2160_30_yuv420p.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 3840 -h 2160"
                print command_imgalign
                subprocess.call(command_imgalign)
                
            elif testfile[i] == "4k_danren":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_4K\\Marked_danren_3840x2160_30_yuv420p.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 3840 -h 2160"
                print command_imgalign
                subprocess.call(command_imgalign)  
                
            elif testfile[i] == "4k_mianbutexie":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_4K\\Marked_mianbutexie_3840x2160_yuv420p_30.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 3840 -h 2160"
                print command_imgalign
                subprocess.call(command_imgalign)
                
            elif testfile[i] == "4k_jinchang":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_4K\\Marked_jinchang_3840x2160_yuv420p.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 3840 -h 2160"
                print command_imgalign
                subprocess.call(command_imgalign) 
                
            elif testfile[i] == "4k_pingyi":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_4K\\Marked_pingyi_3840x2160_30.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 3840 -h 2160"
                print command_imgalign
                subprocess.call(command_imgalign)  
                
            elif testfile[i] == "4k_ruzuo":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_4K\\Marked_ruzuo_yuv420p_3840x2160_30.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 3840 -h 2160"
                print command_imgalign
                subprocess.call(command_imgalign) 
                
            elif testfile[i] == "4k_excel":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_4K\\Marked_excel_3840x2160_30_yuv420p.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 3840 -h 2160"
                print command_imgalign
                subprocess.call(command_imgalign) 
                
            elif testfile[i] == "4k_word":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_4K\\Marked_word_3840x2160_30_yuv420p.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 3840 -h 2160"
                print command_imgalign
                subprocess.call(command_imgalign)
                
            elif testfile[i] == "4k_ppt":
                command_imgalign = "imgalign.exe -m 1 -d 6 --margin 1 -s D:\\VideoTestFileall\\Marked_4K\\Marked_ppt_3840x2160_30_yuv420p.yuv -p " + dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv" + " -w 3840 -h 2160"
                print command_imgalign
                subprocess.call(command_imgalign)
                
            else :
                print "Error:No such file!"                                
            
            print "command_imgalign over!"
            
            
            #-------------------------framerate计算帧率-------------------------#
            
            if os.path.exists('cmp_out_cooked-2.yuv'):

                outcookedfile = os.getcwd() + "\cmp_out_cooked-2.yuv"
                File.append(outcookedfile)
                outorifile = os.getcwd() + "\cmp_out_ori-2.yuv"
                File.append(outorifile)
                outlogfile = os.getcwd() + "\imgalign-2.log"
                File.append(outlogfile)  
                
            else:
                outcookedfile = os.getcwd() + "\cmp_out_cooked-1.yuv"
                File.append(outcookedfile)
                outorifile = os.getcwd() + "\cmp_out_ori-1.yuv"
                File.append(outorifile)
                outlogfile = os.getcwd() + "\imgalign-1.log"
                File.append(outlogfile)                  
                
                
            command_framerate = "framerate.exe " + str(OrgFrame) + " " +outlogfile 
            subprocess.call(command_framerate)
            
            print "command_framerate over!"        
           
            outFps = os.getcwd() + "\FPS.txt"
            File.append(outFps)
            outFpsavg = os.getcwd() + "\FPSAvg.txt" 
            File.append(outFpsavg)
            
            #-------移动文件至对应的文件夹内-------#
            for srcfile in File:
                    MoveFile(srcfile, dstfile)
                    
          
            #-------------------------------开始重新计算帧率---------------------------------#
            
            filename = dstfile + '\NewFPS.txt'
            FPS = []
            fileFps = open(dstfile+"\FPS.txt")
            sum1 = 0
            fpsSum = 0
            fpsSTDEVP = 0
            
            #从FPS中读取每秒的帧率,并存放到列表中
            for line in fileFps:
                fps = re.findall(r"\d+\.?\d*",line)  #匹配数值
                #print fps[1]
                FPS1 = FPS.append(int(fps[1]))
            print "oldFPS:" + str(FPS)
            
            if testfile[i] == "duoren":
                testfileFrameCount = 720
                
            elif testfile[i] == "duoren_30fps":
                testfileFrameCount = 900                 
                
            elif testfile[i] == "danren":
                testfileFrameCount = 720
                
            elif testfile[i] == "excel":
                testfileFrameCount = 300
                
            elif testfile[i] == "excel_60fps":
                testfileFrameCount = 600            
                
            elif testfile[i] == "word":
                testfileFrameCount = 300
                
            elif testfile[i] == "ppt":
                testfileFrameCount = 300
                
            elif testfile[i] == "bag":
                testfileFrameCount = 570
                
            elif testfile[i] == "ducks":
                testfileFrameCount = 500
                
            elif testfile[i] == "park":
                testfileFrameCount = 222
                
            elif testfile[i] == "pass":
                testfileFrameCount = 570
                
            elif testfile[i] == "run":
                testfileFrameCount = 500
                
            elif testfile[i] == "trailer":
                testfileFrameCount = 1253
                
            elif testfile[i] == "tree":
                testfileFrameCount = 500
                
            elif testfile[i] == "4k_duoren":
                testfileFrameCount = 450   
                
            elif testfile[i] == "4k_danren":
                testfileFrameCount = 450 
                
            elif testfile[i] == "4k_mianbutexie":
                testfileFrameCount = 181
                
            elif testfile[i] == "4k_jinchang":
                testfileFrameCount = 211  
                
            elif testfile[i] == "4k_pingyi":
                testfileFrameCount = 211  
                
            elif testfile[i] == "4k_ruzuo":
                testfileFrameCount = 211      
                
            elif testfile[i] == "4k_excel":
                testfileFrameCount = 300  
                
            elif testfile[i] == "4k_word":
                testfileFrameCount = 300  
                
            elif testfile[i] == "4k_ppt":
                testfileFrameCount = 300              
                
            else:
                print "No Such TestFileFrameCount!"       
                
            #判断最后一帧是否为完整的一帧，不是则重新算最后一帧帧率，得出新的帧数并输出到txt文档中
            mm = int(testfileFrameCount) % int(OrgFrame)
            #print "mm:" + str(mm)
            #print "FPS[-1]:" + str(FPS[-1])
            if mm != 0 :                
                LastFrame = int((float(FPS[-1]) / mm) * 60)
                #print "LastFrame:" + str(LastFrame)
                FPS[-1] = LastFrame       
                print "NewFPS:" + str(FPS)
                text_save(filename, FPS)  
            
            #取出帧率的最大值和最小值    
            Max = max(FPS)
            Min = min(FPS)            
            print "Max FrameRate:" + str(Max)
            print "Min FrameRate:" + str(Min)
             #计算帧率平均值   
            for a in range(len(FPS)):        
                sum1 = FPS[a] +sum1
            #print sum1
            avgFps = float(sum1)/ len(FPS)    
            print "avgFps:" + str(avgFps)
            
            #计算帧率的方差
            for b in range(len(FPS)):        
                fpsPer = abs(float(FPS[b]) - float(avgFps))
                fps2 = fpsPer * fpsPer
                fpsSum = fpsSum +fps2
            fpsVariance = math.sqrt((fpsSum/len(FPS)))
            print "fpsVariance:" + str(fpsVariance)   
            
            #帧率输出csv模块
            csvresult = file(dstfile+"\New_FrameRateResult_" + testfile[i] + "_" + data[j] + ".csv", 'ab')            
            writer = csv.writer(csvresult)
            writer.writerow(['fileInfo', 'fpsAvg', 'fpsVariance','MaxFrameRate','MinFrameRate'])
            writer.writerow([dstfile,str(avgFps),str(fpsVariance),str(Max),str(Min)])    
            
            time.sleep(20)          
            
            #删除对齐后生成的其他的yuv、log等文件
            deleteFile()
            
            #删除data转成YUV的文件
            os.remove(dstfile + "\\" + DataName + "_" + testfile[i] + "_" + data[j] +".yuv")
            
    
    

                
        
        
        
    







