# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Administrator\Desktop\aec.ui'
#
# Created: Wed Aug 02 14:00:06 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import task
import taskThread
import os
import subprocess
import time
import re
import sys
#*******************************以下代码为界面生成的代码******************
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Administrator\Desktop\aec.ui'
#
# Created: Tue Aug 01 15:03:12 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindows(object):
    def setupUi(self, MainWindows):
        MainWindows.setObjectName(_fromUtf8("MainWindows"))
        MainWindows.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindows)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 40, 151, 41))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(430, 90, 151, 41))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 90, 161, 41))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(430, 140, 151, 41))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 140, 151, 41))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(380, 40, 201, 41))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(290, 0, 221, 41))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(80, 200, 151, 41))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(320, 200, 151, 41))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.start = QtGui.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(110, 440, 75, 23))
        self.start.setObjectName(_fromUtf8("start"))
        self.stop = QtGui.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(590, 440, 75, 23))
        self.stop.setObjectName(_fromUtf8("stop"))
        self.mt_type = QtGui.QComboBox(self.centralwidget)
        self.mt_type.setGeometry(QtCore.QRect(100, 240, 101, 22))
        self.mt_type.setObjectName(_fromUtf8("mt_type"))
        self.mt_type.addItem(_fromUtf8(""))
        self.mt_type.addItem(_fromUtf8(""))
        self.test_mode = QtGui.QComboBox(self.centralwidget)
        self.test_mode.setGeometry(QtCore.QRect(360, 240, 69, 22))
        self.test_mode.setObjectName(_fromUtf8("test_mode"))
        self.test_mode.addItem(_fromUtf8(""))
        self.test_mode.addItem(_fromUtf8(""))
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(540, 200, 151, 41))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(540, 290, 151, 41))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.test_file = QtGui.QComboBox(self.centralwidget)
        self.test_file.setGeometry(QtCore.QRect(540, 240, 151, 22))
        self.test_file.setObjectName(_fromUtf8("test_file"))
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(510, 310, 51, 61))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(570, 310, 51, 61))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_14 = QtGui.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(630, 310, 51, 61))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_15 = QtGui.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(720, 310, 71, 61))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.host = QtGui.QLineEdit(self.centralwidget)
        self.host.setGeometry(QtCore.QRect(190, 50, 171, 20))
        self.host.setObjectName(_fromUtf8("host"))
        self.port = QtGui.QLineEdit(self.centralwidget)
        self.port.setGeometry(QtCore.QRect(580, 50, 171, 20))
        self.port.setObjectName(_fromUtf8("port"))
        self.tel_un = QtGui.QLineEdit(self.centralwidget)
        self.tel_un.setGeometry(QtCore.QRect(190, 100, 171, 20))
        self.tel_un.setObjectName(_fromUtf8("tel_un"))
        self.tel_pw = QtGui.QLineEdit(self.centralwidget)
        self.tel_pw.setGeometry(QtCore.QRect(580, 100, 171, 20))
        self.tel_pw.setObjectName(_fromUtf8("tel_pw"))
        self.ftp_un = QtGui.QLineEdit(self.centralwidget)
        self.ftp_un.setGeometry(QtCore.QRect(190, 150, 171, 20))
        self.ftp_un.setObjectName(_fromUtf8("ftp_un"))
        self.ftp_pw = QtGui.QLineEdit(self.centralwidget)
        self.ftp_pw.setGeometry(QtCore.QRect(580, 150, 171, 20))
        self.ftp_pw.setObjectName(_fromUtf8("ftp_pw"))
        self.H = QtGui.QLineEdit(self.centralwidget)
        self.H.setGeometry(QtCore.QRect(490, 330, 31, 21))
        self.H.setText(_fromUtf8(""))
        self.H.setObjectName(_fromUtf8("H"))
        self.M = QtGui.QLineEdit(self.centralwidget)
        self.M.setGeometry(QtCore.QRect(550, 330, 31, 21))
        self.M.setText(_fromUtf8(""))
        self.M.setObjectName(_fromUtf8("M"))
        self.S = QtGui.QLineEdit(self.centralwidget)
        self.S.setGeometry(QtCore.QRect(610, 330, 31, 21))
        self.S.setText(_fromUtf8(""))
        self.S.setObjectName(_fromUtf8("S"))
        self.MS = QtGui.QLineEdit(self.centralwidget)
        self.MS.setGeometry(QtCore.QRect(670, 330, 61, 21))
        self.MS.setText(_fromUtf8(""))
        self.MS.setObjectName(_fromUtf8("MS"))
        self.label_16 = QtGui.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(80, 290, 151, 41))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.aud_device = QtGui.QComboBox(self.centralwidget)
        self.aud_device.setGeometry(QtCore.QRect(80, 330, 161, 22))
        self.aud_device.setObjectName(_fromUtf8("aud_device"))
        MainWindows.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindows)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindows.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindows)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindows.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindows)
        QtCore.QMetaObject.connectSlotsByName(MainWindows)
        
        #*******************************以上代码为界面生成的代码************************ 
        
        
        #***************************将start按钮与开始任务函数绑定，即点击开始按钮，任务开始执行************       
        self.start.clicked.connect(self.startTask)
        #self.stop.clicked.connect(quit())
        self.stop.connect(self.stop, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
        
        self.mt_type.currentIndexChanged.connect(self.mtTypeChanged)
        #*******************************以下代码为界面生成的代码************************    

    def retranslateUi(self, MainWindows):
        MainWindows.setWindowTitle(_translate("MainWindows", "MainWindow", None))
        self.label.setText(_translate("MainWindows", "<html><head/><body><p align=\"right\"><span style=\" font-size:14pt;\">IP：</span></p></body></html>", None))
        self.label_2.setText(_translate("MainWindows", "<html><head/><body><p align=\"right\"><span style=\" font-size:14pt;\">telnet密码：</span></p></body></html>", None))
        self.label_3.setText(_translate("MainWindows", "<html><head/><body><p align=\"right\"><span style=\" font-size:14pt;\">telnet用户名：</span></p></body></html>", None))
        self.label_4.setText(_translate("MainWindows", "<html><head/><body><p align=\"right\"><span style=\" font-size:14pt;\">ftp密码：</span></p></body></html>", None))
        self.label_5.setText(_translate("MainWindows", "<html><head/><body><p align=\"right\"><span style=\" font-size:14pt;\">ftp用户名：</span></p></body></html>", None))
        self.label_6.setText(_translate("MainWindows", "<html><head/><body><p align=\"right\"><span style=\" font-size:14pt;\">telnet端口号：</span></p></body></html>", None))
        self.label_7.setText(_translate("MainWindows", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">AEC端终端配置信息</span></p></body></html>", None))
        self.label_10.setText(_translate("MainWindows", "<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600;\">测试终端类型</span></p></body></html>", None))
        self.label_11.setText(_translate("MainWindows", "<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600;\">AEC测试模式</span></p></body></html>", None))
        self.start.setText(_translate("MainWindows", "开始", None))
        self.stop.setText(_translate("MainWindows", "停止", None))
        self.mt_type.setItemText(0, _translate("MainWindows", "我司终端", None))
        self.mt_type.setItemText(1, _translate("MainWindows", "外厂商终端", None))
        self.test_mode.setItemText(0, _translate("MainWindows", "单讲", None))
        self.test_mode.setItemText(1, _translate("MainWindows", "双讲", None))
        self.label_12.setText(_translate("MainWindows", "<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600;\">选择测试序列</span></p></body></html>", None))
        self.label_13.setText(_translate("MainWindows", "<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600;\">定时启动时间</span></p></body></html>", None))
        self.label_8.setText(_translate("MainWindows", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">时</span></p></body></html>", None))
        self.label_9.setText(_translate("MainWindows", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">分</span></p></body></html>", None))
        self.label_14.setText(_translate("MainWindows", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">秒</span></p></body></html>", None))
        self.label_15.setText(_translate("MainWindows", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">毫秒</span></p></body></html>", None))
        self.label_16.setText(_translate("MainWindows", "<html><head/><body><p align=\"right\"><span style=\" font-size:18pt; font-weight:600;\">选择声卡设备</span></p></body></html>", None))
        

    #*******************************以上代码为界面生成的代码************************
    
    #*******************************读取ref_file并添加到combobox里************************
        i=0
        for root, dirs, files in os.walk("D:/AEC_Auto_test/ref_file"):
            for name in files:
                #print name
                self.test_file.addItem(_fromUtf8(""))
                self.test_file.setItemText(i, _translate("MainWindows", name, None))
                i=i+1
    
    #*******************************读取声卡设备并添加到combobox里************************         
        out=subprocess.Popen("D:\\AEC_Auto_test\\ffmpeg.exe -list_devices true -f dshow -i dummy",shell=True,stderr=subprocess.PIPE)
        alllines = out.stderr.read()
        word = "DirectShow audio devices"
        a = [m.start() for m in re.finditer(word,alllines)]
        def GetMiddleStr(content,startStr,endStr):
            startIndex = content.index(startStr)
            if startIndex>=0:
                startIndex += len(startStr)
                endIndex = content.index(endStr)
                return content[startIndex:endIndex]
        #if __name__=='__main__':
        audio= GetMiddleStr(alllines,'DirectShow audio devices','dummy: Immediate exit requested')
    #print audio
        sts = audio.split('"')
        lng=len(sts)//4
        z=0
        for x in range(1,lng+1):
            st=sts[4*x-3]
            #print st
            #st ="麦克风 (Realtek High Definition Au"
            self.aud_device.addItem(_fromUtf8(""))
            self.aud_device.setItemText(z, _translate("MainWindows", st, None)) 
            z=z+1
    
    #****************************自定义界面处理函数，即获取编辑框中的内容和开始任务**********
    def getHostIP(self, MainWindow):
        return self.host.text()
    def getHostPort(self, MainWindow):
        return self.port.text()  

    def getTelUsrName(self, MainWindow):
        return self.tel_un.text()
    def getTelUsrPwd(self, MainWindow):
        return self.tel_pw.text()
    def getFtpUsrName(self, MainWindow):
        return self.ftp_un.text()
    def getFtpUsrPwd(self, MainWindow):
        return self.ftp_pw.text()

    def getH(self, MainWindow):
        return self.H.text()  
    def getM(self, MainWindow):
        return self.M.text() 
    def getS(self, MainWindow):
        return self.S.text() 
    def getMS(self, MainWindow):
        return self.MS.text()     

#*************索引从0开始**************
    def getMtType(self, MainWindow):
        mt = self.mt_type.currentIndex() 
        return mt            
            
    def getTestMode(self, MainWindow):
        if self.test_mode.currentIndex() == 0:
            return 's'
        else :
            return 'd'
        
    def getTestFile(self, MainWindow):
        test_file=str(self.test_file.currentText())
        #print strtest_file
        #commandref='D:\\AEC_Auto_test\\AECResultAutoAnalysis.exe ' + 'D:\\AEC_Auto_test\\ref_file\\' + strtest_file + ' 48000 -60' 
        #print commandref
        return test_file
    
    def getaud_device(self, MainWindow):
        reload(sys)                        
        sys.setdefaultencoding('utf-8')        
        aud_device=str(self.aud_device.currentText())
        return aud_device   
    
  #********************我司终端可编辑外厂商终端只读******************  
    def mtTypeChanged(self, MainWindow):
        mt = self.mt_type.currentIndex()
        if mt == 1 :
            self.host.setReadOnly(True)
            self.port.setReadOnly(True)
            self.tel_un.setReadOnly(True)
            self.tel_pw.setReadOnly(True)
            self.ftp_un.setReadOnly(True)
            self.ftp_pw.setReadOnly(True) 
        else:
            self.host.setReadOnly(False)
            self.port.setReadOnly(False)
            self.tel_un.setReadOnly(False)
            self.tel_pw.setReadOnly(False)
            self.ftp_un.setReadOnly(False)
            self.ftp_pw.setReadOnly(False)             
            
        
    def startTask(self, MainWindow):
        #mt,mode,host,port,tel_un,tel_pw,ftp_un,ftp_pw，H，M，S，MS
        mt = self.getMtType(MainWindow)
        mode = self.getTestMode(MainWindow)
        host = self.getHostIP(MainWindow)
        port = self.getHostPort(MainWindow)
        tel_un = self.getTelUsrName(MainWindow)
        tel_pw = self.getTelUsrPwd(MainWindow)
        ftp_un = self.getFtpUsrName(MainWindow)
        ftp_pw = self.getFtpUsrPwd(MainWindow)
        H = self.getH(MainWindow)
        M = self.getM(MainWindow)
        S = self.getS(MainWindow)
        MS = self.getMS(MainWindow)
        ref_file = self.getTestFile(MainWindow)
        aud_device=self.getaud_device(MainWindow)
        self.Taskthread = taskThread.taskThread(task.task,mt,mode,host,port,tel_un,tel_pw,ftp_un,ftp_pw,H,M,S,MS,ref_file,aud_device)
        self.Taskthread.start()


