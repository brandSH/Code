from PyQt4.QtCore import *

class taskThread(QThread):
    def __init__(self,taskfunc,mt,mode,host,port,tel_un,tel_pw,ftp_un,ftp_pw,H,M,S,MS,ref_file,aud_device):
        super(taskThread,self).__init__()
        self.taskfunc = taskfunc
        self.mt = mt
        self.mode = mode
        self.host = host
        self.port = port 
        self.tel_un = tel_un
        self.tel_pw = tel_pw
        self.ftp_un = ftp_un
        self.ftp_pw = ftp_pw
        self.H = H
        self.M = M
        self.S = S
        self.MS = MS
        self.test_file = ref_file
        self.aud_device = aud_device
    def run(self):
        self.taskfunc(self.mt,self.mode,self.host,self.port,self.tel_un,self.tel_pw,self.ftp_un,self.ftp_pw,self.H,self.M,self.S,self.MS,self.test_file,self.aud_device)
