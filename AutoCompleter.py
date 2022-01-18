# from PyQt6.QtCore import QAbstractListModel, QFile, QModelIndex, QStringListModel, Qt
# from PyQt6.QtGui import QCursor, QKeySequence, QTextCursor, QAction
# from PyQt6.QtWidgets import QApplication, QCompleter, QMainWindow, QMessageBox, QTextEdit
# import sys

# from readingcsv import unloading

# class TextEdit(QTextEdit):
#     def __init__(self, parent=None):
#         super(TextEdit, self).__init__(parent)

#         self._completer = None

#         self.setPlainText(
#             "This TextEdit provides autocompletions for words that have "
#             "more than 3 characters. You can trigger autocompletion "
#             "using %s" % QKeySequence("Ctrl+E").toString(
#                 QKeySequence.SequenceFormat.NativeText))

#     def setCompleter(self, c):
#         if self._completer is not None:
#             self._completer.activated.disconnect()

#         self._completer = c

#         c.setWidget(self)
#         c.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
#         c.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
#         c.activated.connect(self.insertCompletion)

#     def completer(self):
#         return self._completer

#     def insertCompletion(self, completion):
#         if self._completer.widget() is not self:
#             return

#         tc = self.textCursor()
#         extra = len(completion) - len(self._completer.completionPrefix)
#         tc.movePosition(QTextCursor.MoveOperation.Left)
#         tc.movePosition(QTextCursor.MoveOperation.EndOfWord)
#         tc.insertText(completion[-extra:])
#         self.setTextCursor(tc)

#     def textUnderCursor(self):
#         tc = self.textCursor()
#         tc.select(QTextCursor.SelectionType.WordUnderCursor)

#         return tc.selectedText()

#     def focusInEvent(self, e):
#         if self._completer is not None:
#             self._completer.setWidget(self)

#         super(TextEdit, self).focusInEvent(e)

#     def keyPressEvent(self, e):
#         if self._completer is not None and self._completer.popup().isVisible():
#             # The following keys are forwarded by the completer to the widget.
#             if e.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return,
#                            Qt.Key.Key_Escape, Qt.Key.Key_Tab,
#                            Qt.Key.Key_Backtab):
#                 e.ignore()
#                 # Let the completer do default behavior.
#                 return

#         isShortcut = (
#             (e.modifiers() & Qt.KeyboardModifier.ControlModifier) != 0
#             and e.key() == Qt.Key.Key_E)
#         if self._completer is None or not isShortcut:
#             # Do not process the shortcut when we have a completer.
#             super(TextEdit, self).keyPressEvent(e)

#         ctrlOrShift = e.modifiers() & (Qt.KeyboardModifier.ControlModifier
#                                        | Qt.KeyboardModifier.ShiftModifier)
#         if self._completer is None or (ctrlOrShift and len(e.text()) == 0):
#             return

#         eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="
#         hasModifier = (e.modifiers() !=
#                        Qt.KeyboardModifier.NoModifier) and not ctrlOrShift
#         completionPrefix = self.textUnderCursor()

#         if not isShortcut and (hasModifier or len(e.text()) == 0
#                                or len(completionPrefix) < 3
#                                or e.text()[-1] in eow):
#             self._completer.popup().hide()
#             return

#         if completionPrefix != self._completer.completionPrefix():
#             self._completer.setCompletionPrefix(completionPrefix)
#             self._completer.popup().setCurrentIndex(
#                 self._completer.completionModel().index(0, 0))

#         cr = self.cursorRect()
#         cr.setWidth(
#             self._completer.popup().sizeHintForColumn(0) +
#             self._completer.popup().verticalScrollBar().sizeHint().width())
#         self._completer.complete(cr)

# class MainWindow(QMainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)

#         self.createMenu()

#         self.completingTextEdit = TextEdit()
#         self.completer = QCompleter(self)
#         self.completer.setModel(self.modelFromFile())
#         self.completer.setModelSorting(
#             QCompleter.ModelSorting.CaseInsensitivelySortedModel)
#         self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
#         self.completer.setWrapAround(False)
#         self.completingTextEdit.setCompleter(self.completer)

#         self.setCentralWidget(self.completingTextEdit)
#         self.resize(500, 300)
#         self.setWindowTitle("Completer")

#     def createMenu(self):
#         exitAction = QAction("Exit", self)
#         aboutAct = QAction("About", self)
#         aboutQtAct = QAction("About Qt", self)

#         exitAction.triggered.connect(QApplication.instance().quit)
#         aboutAct.triggered.connect(self.about)
#         aboutQtAct.triggered.connect(QApplication.instance().aboutQt)

#         fileMenu = self.menuBar().addMenu("File")
#         fileMenu.addAction(exitAction)

#         helpMenu = self.menuBar().addMenu("About")
#         helpMenu.addAction(aboutAct)
#         helpMenu.addAction(aboutQtAct)

#     def modelFromFile(self):

#         QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
#         data = unloading()
#         words = []
#         for i, j in data.items():
#             for a in j:
#                 words.append(i + "  " + a)
#         QApplication.restoreOverrideCursor()

#         return QStringListModel(words, self.completer)

#     def about(self):
#         QMessageBox.about(
#             self, "About",
#             "This example demonstrates the different features of the "
#             "QCompleter class.")

# if __name__ == '__main__':

#     import sys

#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QStandardItem


def create_model(d):
    # a=QtCore.QModelIndex()

    model = QtGui.QStandardItemModel()
    for key, value in d.items():
        for val in value:
            it = QtGui.QStandardItem(key)
            it.setData(val, QtCore.Qt.ItemDataRole.UserRole)
            model.appendRow(it)
    return model


class StyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(StyledItemDelegate, self).initStyleOption(option, index)
        option.text = index.data(QtCore.Qt.ItemDataRole.UserRole)


class Completer(QtWidgets.QCompleter):
    def __init__(self, parent=None):
        super(Completer, self).__init__(parent)
        QtCore.QTimer.singleShot(0, self.change_delegate)

    @QtCore.pyqtSlot()
    def change_delegate(self):
        delegate = StyledItemDelegate(self)
        self.popup().setItemDelegate(delegate)

    def pathFromIndex(self, index):
        return index.data(QtCore.Qt.ItemDataRole.UserRole)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    d = {"George": ["Washington", "Bush"], "Languages": ["Python", "C++"]}
    model = create_model(d)
    w = QtWidgets.QLineEdit()
    completer = Completer(w)
    completer.setModel(model)
    w.setCompleter(completer)
    w.show()
    sys.exit(app.exec())