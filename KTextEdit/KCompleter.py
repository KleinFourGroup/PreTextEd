from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore

class KCompleter(QtWidgets.QCompleter): 
    insertText = QtCore.pyqtSignal(str)
    
    def __init__(self, myKeywords=None,parent=None):
        # TODO: Ugh
        myKeywords =['apple','aggresive','ball','bat','cat','cycle','dog','dumb',\
                     'elephant','engineer','food','file','good','great',\
                     'hippopotamus','hyper','india','ireland','just','just',\
                     'key','kid','lemon','lead','mute','magic',\
                     'news','newyork','orange','oval','parrot','patriot',\
                     'question','queue','right','rest','smile','simple',\
                     'tree','urban','very','wood','xylophone','yellow',\
                     'zebra']
        QtWidgets.QCompleter.__init__(self, myKeywords, parent)
        # Wut
        self.connect(self, QtCore.SIGNAL("activated(const QString&)"), self.changeCompletion)

    def changeCompletion(self, completion):
        if completion.find("(") != -1:
            completion = completion[:completion.find("(")]
        print(completion)
        self.insertText.emit(completion)
