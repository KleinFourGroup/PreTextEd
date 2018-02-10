import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
# import QMainWindow, QDesktopWidget, QApplication

kmap = {
    Qt.Key_U : ['a', 'b', 'c'],
    Qt.Key_I : ['d', 'e', 'f'],
    Qt.Key_O : ['g', 'h', 'i'],
    Qt.Key_P : ['j', 'k', 'l'],
    Qt.Key_J : ['m', 'n', 'o'],
    Qt.Key_K : ['p', 'q', 'r', 's'],
    Qt.Key_L : ['t', 'u', 'v'],
    Qt.Key_M : ['w', 'x', 'y', 'z']
    }

class KKeyEvent(QtGui.QKeyEvent):
    pass

class MTBuffer(QtCore.QObject):

    flushEvent = QtCore.pyqtSignal(str) # ???

    def __init__(self, sb):
        super().__init__()
        self.sb = sb
        self.mutex = QtCore.QMutex()
        self.snum = 0
        self.timer = None
        self.key = None
        self.count = -1

    def contents(self):
        return "%d" % snum
    
    def flush(self, hasLock = False, snum = None):
        # print("[buff] flush(%s, %s)" % (str(hasLock), str(snum)))
        if not hasLock:
            self.mutex.lock()
        if snum and (not snum == self.snum):
            pass
        ## ALL CLEAR ##
        elif self.key in kmap:
            char = kmap[self.key][self.count]
            self.flushEvent.emit(char)
            self.key = None
            self.count = -1
            self.sb.showMessage("Flushed: '%c'" % char)
        if not hasLock:
            self.mutex.unlock()

    def push(self, event):
        self.mutex.lock()
        key = event.key()
        # print("[buff] got %d" % key)
        if (not key == self.key) or (key == self.key and self.count == len(kmap[key]) - 1):
            self.flush(True)
            self.key = None
            self.count = -1
        if key in kmap:
            self.snum += 1
            snum = self.snum
            self.key = key
            self.count += 1
            if self.timer:
                self.timer.stop()
                self.timer.deleteLater()
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(lambda : self.flush(False, snum))
            self.timer.setSingleShot(True)
            self.timer.start(1000)
            self.sb.showMessage("Current: '%c'" % kmap[self.key][self.count])
        self.mutex.unlock()
    
class Example(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.buff = MTBuffer(self.sb)
        self.buff.flushEvent.connect(self.getFlush)
        
        
    def initUI(self):               
        self.sb = self.statusBar()
        self.sb.showMessage('Test')
        self.edit = QtWidgets.QTextEdit()

        #QtWidgets.qApp.installEventFilter(self)
        self.edit.installEventFilter(self)
        
        self.setCentralWidget(self.edit)
        self.resize(250, 150)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        self.setWindowTitle('Multi-tap')    
        self.show()

    def getFlush(self, char):
        #print("Flushed '%c'" % char)
        obj = QtWidgets.QApplication.focusWidget()
        self.sendkeys(obj, char)
        
    def sendkeys(self, obj, char, modifier=Qt.NoModifier):
        #print("Sending '%c'" % char)
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, 0, modifier, char)
        QtCore.QCoreApplication.postEvent(obj, event)
        event = QtGui.QKeyEvent(QtCore.QEvent.KeyRelease, 0, modifier, char)
        QtCore.QCoreApplication.postEvent(obj, event)

    def eventFilter(self, obj, event):
        if type(event) == QtGui.QKeyEvent:
            # print("Normal stroke %d of type %s to %s (focus %s)" % (event.key(), str(event.type()), str(obj), str(QtWidgets.QApplication.focusWidget())))
            if event.key() in kmap and obj == QtWidgets.QApplication.focusWidget():
                if event.type() == QtCore.QEvent.KeyPress:
                    self.buff.push(event)
                return True #event.ignore()
        return super().eventFilter(obj, event) #event.accept()
         
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
