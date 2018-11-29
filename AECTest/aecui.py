import sys,pdb
from PyQt4 import  QtCore, QtGui
import aec
#from aec import Ui_MainWindows
 
class AecWnd(QtGui.QMainWindow,aec.Ui_MainWindows): 
    def __init__(self, parent=None): 
        super(AecWnd, self).__init__(parent) 
        wnd = self.setupUi(self)
         
def mywindow():   
    mywindow = AecWnd()
    mywindow.show()
    return mywindow
     
app = QtGui.QApplication( sys.argv )
myobj = mywindow()    
sys.exit(app.exec_())  
