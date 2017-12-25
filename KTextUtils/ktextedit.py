from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

from kcompleter import KCompleter

class KTextEdit(QtWidgets.QTextEdit):
    
    def __init__(self,*args):
        #*args to set parent
        QtWidgets.QLineEdit.__init__(self,*args)
        font=QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.completer = None

    def setCompleter(self, completer):
        if self.completer:
            self.disconnect(self.completer, 0, self, 0)
        if not completer:
            return
        completer.setWidget(self)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer = completer
        self.completer.insertText.connect(self.insertCompletion)
        
    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (len(completion) - len(self.completer.completionPrefix()))
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)
        
    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()
    
    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QtWidgets.QTextEdit.focusInEvent(self, event)

    # TODO: Refactor.  Looks iffy
    def keyPressEvent(self, event):
        if self.completer and self.completer.popup() and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter,
                               Qt.Key_Return,
                               Qt.Key_Escape,
                               Qt.Key_Tab,
                               Qt.Key_Backtab):
                event.ignore()
                return
        # has ctrl-Space been pressed??
        isShortcut = (event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Space)
        # modifier to complete suggestion inline ctrl-e
        inline = (event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_E)
        # if inline completion has been chosen
        if inline:
            # set completion mode as inline
            self.completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
            completionPrefix = self.textUnderCursor()
            if (completionPrefix != self.completer.completionPrefix()):
                self.completer.setCompletionPrefix(completionPrefix)
            self.completer.complete()
            # set the current suggestion in the text box
            self.completer.insertText.emit(self.completer.currentCompletion())
            # reset the completion mode
            self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            return
        if (not self.completer or not isShortcut):
            pass
            QtWidgets.QTextEdit.keyPressEvent(self, event)
        ## ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (Qt.ControlModifier, Qt.ShiftModifier)
        if ctrlOrShift and event.text()== '':
            return
        eow = "~!@#$%^&*+{}|:\"<>?,./;'[]\\-=" #end of word

        hasModifier = ((event.modifiers() != Qt.NoModifier) and not ctrlOrShift)

        completionPrefix = self.textUnderCursor()
        if not isShortcut :
            if self.completer.popup():
                self.completer.popup().hide()
            return
        self.completer.setCompletionPrefix(completionPrefix)
        popup = self.completer.popup()
        popup.setCurrentIndex(self.completer.completionModel().index(0,0))
        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr) ## popup it up!

"""
if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    completer = KCompleter()
    te = KTextEdit()
    te.setCompleter(completer)
    te.show()
    app.exec_()
"""
