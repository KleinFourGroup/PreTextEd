import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
# import QMainWindow, QDesktopWidget, QApplication

kmap = [Qt.Key_U,Qt.Key_I,Qt.Key_O,Qt.Key_P,Qt.Key_J,Qt.Key_K,Qt.Key_L,Qt.Key_M]

class Example(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):               
        self.edit = QtWidgets.QTextEdit()

        QtWidgets.qApp.installEventFilter(self)
        
        self.setCentralWidget(self.edit)
        self.resize(250, 150)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Event Test')    
        self.show()
        
    def sendkeys(self, obj, char, modifier=Qt.NoModifier):
        print("Sending '%c'" % char)
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, 0, modifier, char)
        QtCore.QCoreApplication.postEvent(obj, event)
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyRelease, 0, modifier, char)
        QtCore.QCoreApplication.postEvent(obj, event)

    def eventFilter(self, obj, event):
        if type(event) == QtGui.QKeyEvent:
            print("Normal stroke %d of type %s to %s (focus %s)" % (event.key(), str(event.type()), str(obj), str(QtWidgets.QApplication.focusWidget())))
            if event.key() in kmap and obj == QtWidgets.QApplication.focusWidget():
                if event.type() == QtCore.QEvent.KeyPress:
                    self.sendkeys(obj, "c")
                return True #event.ignore()
        return super().eventFilter(obj, event) #event.accept()
         
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
