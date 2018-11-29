# -*- coding: gbk -*-

from pywinauto import application
import pyautogui as pag
import time
import win32gui
import win32api
import psutil 
import os

#--------------------获取焦点----------------#   
def GetFouce(classname, titlename):
    #窗口最小化时不能获得焦点
    app = application.Application().connect(title_re=titlename)    
    appWindow = app[titlename]
    appWindow.Maximize()    
    #classname, titlename使用Spy++获取
    #获取句柄
    hwnd = win32gui.FindWindow(classname, titlename)
    win32gui.SetForegroundWindow(hwnd)
    
    
#--------------------获取进程CPU使用率（单位是逻辑核）----------------#  
def GetAppCPUPercent(App_Name):
    procs = psutil.process_iter()
    for proc in procs:
        #App_Name = proc.name()
        if App_Name == proc.name():
            return proc.cpu_percent()
         

#--------------------侦测到窗口存在后跳出----------------#  
def WindowExistDo(title):
    e = 0
    while e == 0:
        try:
            OpenFile = application.Application().connect(title_re = title)
            return OpenFile
        except:
            time.sleep(1)

#--------------------侦测到窗口不存在后跳出----------------#  
def WindowNonExistDo(title):
    e = 0
    while e == 0:
        try:
            VQC2 = application.Application().connect(title_re = title) 
            time.sleep(1)
        except:
            break  
    
#--------------------打开文件或保存文件----------------#  
def OpenOrSaveFile(WindowTitle,FilePath,Action):
    OpenFile = WindowExistDo(WindowTitle)        
    Edit = OpenFile[WindowTitle][u'ComboBoxEx']
    time.sleep(1)
    Edit.TypeKeys(FilePath)
    time.sleep(1)
    OpenFile = application.Application().connect(title_re = WindowTitle)
    OpenButton = OpenFile[WindowTitle][Action]
    OpenButton.Click()
    time.sleep(1)
    e = 0
    while e == 0:
        try:
            OpenFile = application.Application().connect(title_re = WindowTitle)
            OpenButton = OpenFile[WindowTitle][Action]
            OpenButton.Click()
            time.sleep(1)
        except:
            break  
 

#--------------------打开VQC----------------#   
def StartVQC(VQCExePath):
    Myapp = application.Application().start("\"" + VQCExePath +"\"")
    
    #--------------------VQC启动画面判断(正式版没有这个启动画面)----------------#
    #WindowExistDo('Video Quality Caliper x64')
    #WindowNonExistDo('Video Quality Caliper x64') 
    time.sleep(2)
    VQC = application.Application().connect(title_re=u'Video Quality Caliper')    
    VQCWindow = VQC[r'Video Quality Caliper']
    VQCWindow.Maximize()    

def AddAllYUVandCalculate(YUVFilePathList):
    WindowTitle = r'Open File'
    Action = u'打开(O)'
    #--------------------点击"+File"按钮-----------------#
    for i in range(len(YUVFilePathList)):
        pag.moveTo(30, 240 + 30 * i)
        time.sleep(3)
        pag.click()
        #AddOneYUV(YUVFilePathList[i])
        OpenOrSaveFile(WindowTitle, YUVFilePathList[i], Action)
        WindowNonExistDo('Open File')
    
    time.sleep(1)
    #--------------------点击"Calculate"按钮-----------------#
    pag.moveTo(960, 240 + 30 * (i + 1 ) + 55)
    time.sleep(1)
    pag.click()

#--------------------进入Metric设置-----------------#
def GotoMetrics():
    time.sleep(1)
    pag.moveTo(800, 800)
    time.sleep(1)
    pag.click()
    pag.moveTo(900, 40)
    time.sleep(1)
    pag.click() 
    
#--------------------Metric设置-----------------#
def SetMetrics():
    time.sleep(1)
    #--------------------选择MWDVQM-----------------#
    for i in range(4):
        pag.moveTo(50 + 70*i, 290)
        time.sleep(1)
        pag.click()

    time.sleep(1)
    #--------------------选择MSSIM-----------------#
    for i in range(4):
        pag.moveTo(35 + 60*i, 370)
        time.sleep(1)
        pag.click()
  
#--------------------进入Files设置-----------------#
def GotoFiles():
    time.sleep(1)
    pag.moveTo(800, 800)
    time.sleep(1)
    pag.click()
    pag.moveTo(780, 40)
    time.sleep(1)
    pag.click()       

#--------------------保存CSV文件-----------------#
def SaveCSV(CSVFilePath):
    #--------------------监控VQC的CPU使用率-----------------#
    GetCPUPercentCounts = 0    
    while GetCPUPercentCounts < 90:
        if GetAppCPUPercent(u'VideoQualityCaliper.exe') < 50:
            GetCPUPercentCounts = GetCPUPercentCounts + 1
            time.sleep(1)
        else:
            GetCPUPercentCounts = 0
        
    #--------------------VQC计算结束后保存CSV-----------------# 
    #若未运算结束就保存的CSV是不完整的！
    if GetAppCPUPercent > 5 :        
        time.sleep(2)
        classname = "Qt5QWindowIcon"
        titlename = "Video Quality Caliper"
        GetFouce(classname, titlename)
        time.sleep(1)
        #press区分大小写
        pag.press('f10')
        WindowTitle = r'Save calculation results'
        Action = u'保存(&S)'        
        OpenOrSaveFile(WindowTitle, CSVFilePath, Action) 

#--------------------关闭VQC----------------#  
def KillVQC():
    time.sleep(2)
    procs = psutil.process_iter()
    for proc in procs:
        if proc.name() == 'VideoQualityCaliper.exe':
            proc.kill()

if __name__ == "__main__":
    
    VQCExePath = "C:\Program Files\Intel\Intel(R) Media Server Studio 2017\Video Quality Caliper\VideoQualityCaliper.exe"
    
    
    #------文件目录、测试序列、码率，需要填写------#  
    FilePath = r'D:\1-zp\XMPU5_Video\New_XMPU5_H264_1080P-H265'
    testfile = ["duoren"]     
    data =  ["1M"]
    
    
    for i in range(len(testfile)):
    
        for j in range(len(data)):
            
            if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                   FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
            else:
                YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                   FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
            print YUVFilePathList
            
        
            CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])
            #print CSVFilePath

            StartVQC(VQCExePath)
            GotoMetrics()
            SetMetrics()
            GotoFiles()    
            AddAllYUVandCalculate(YUVFilePathList)
            SaveCSV(CSVFilePath)            
            KillVQC()
            
            #--------------------------------------------------------------------------------判断csv文件里方法是否完整--------------------------------------------------------------------------------#
            
            row2= [row.split(';')[1] for row in open(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')]
            #print row2  
            
            if 'PSNR-Y' in row2:
                print "Metric PSNR-Y is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                
                StartVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()
                
            if 'PSNR-U' in row2:
                print "Metric PSNR-U is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                  
                StartVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()
                
            if 'PSNR-V' in row2:
                print "Metric PSNR-V is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                  
                StartVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()    
                
            if 'PSNR-O' in row2:
                print "Metric PSNR-O is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                  
                StartVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()     
            
            if 'MWDVQM-Y' in row2:
                print "Metric MWDVQM-Y is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                  
                StartVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()     
                
            if 'MWDVQM-U' in row2:
                print "Metric MWDVQM-U is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                  
                StartVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()  
                
            if 'MWDVQM-V' in row2:
                print "Metric MWDVQM-V is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                  
                StartVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()    
                
            if 'MWDVQM-O' in row2:
                print "Metric MWDVQM-O is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                  
                StartVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()     
                
            
            if 'MSSIM-Y' in row2:
                print "Metric MSSIM-Y is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                  
                startVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()   
                
            if 'MSSIM-U' in row2:
                print "Metric MSSIM-U is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                  
                startVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()   
                
            if 'MSSIM-V' in row2:
                print "Metric MSSIM-V is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                  
                startVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()   
                
            if 'MSSIM-O' in row2:
                print "Metric MSSIM-O is exist !"
            else:
                os.remove(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j] + '.csv')
                if os.path.exists(FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv"):
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-2.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-2.yuv")
                else:
                    YUVFilePathList = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_ori-1.yuv",
                                       FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "cmp_out_cooked-1.yuv")                
                print YUVFilePathList           
                CSVFilePath = (FilePath + "\\" + testfile[i] + "\\" + data[j] + "\\" + "VQCResult_" + testfile[i] + "_" + data[j])                  
                startVQC(VQCExePath)
                GotoMetrics()
                SetMetrics()
                GotoFiles()    
                AddAllYUVandCalculate(YUVFilePathList)
                SaveCSV(CSVFilePath)            
                KillVQC()         
            
    
    

