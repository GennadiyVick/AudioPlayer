from PyQt5 import QtCore, QtWidgets, QtGui
import images_rc

class MyLabel(QtWidgets.QLabel):
    onClick = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.onClick.emit()

class MELabel(QtWidgets.QLabel):
    onMousePress = QtCore.pyqtSignal(QtGui.QMouseEvent)
    onMouseMove = QtCore.pyqtSignal(QtGui.QMouseEvent)
    onMouseRelease = QtCore.pyqtSignal(QtGui.QMouseEvent)

    def mousePressEvent(self, event):
        super(MELabel, self).mousePressEvent(event)
        self.onMousePress.emit(event)

    def mouseReleaseEvent(self, event):
        super(MELabel, self).mouseReleaseEvent(event)
        self.onMouseRelease.emit(event)

    def mouseMoveEvent(self, event):
        super(MELabel, self).mouseMoveEvent(event)
        self.onMouseMove.emit(event)

class MyCheckBox(QtWidgets.QLabel):
    toggled = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        super(MyCheckBox,self).__init__(parent)
        self.setMinimumSize(QtCore.QSize(18, 18))
        self.setMaximumSize(QtCore.QSize(18, 18))
        self.setChecked(False)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.setChecked(not self.checked)
            self.toggled.emit()
        super(MyCheckBox, self).mousePressEvent(event)

    def isChecked(self):
        return self.checked

    def setChecked(self, value):
        self.checked = value

        if self.checked:
            self.setStyleSheet('QLabel {background: url(:/images/checked.png) no-repeat;}')
        else:
            self.setStyleSheet('QLabel {background: url(:/images/unchecked.png) no-repeat;}')

class MyComboBox(QtWidgets.QComboBox):
    keyPressed = QtCore.pyqtSignal(QtGui.QKeyEvent)

    def keyPressEvent(self, event):
        if event.key() == 32:
            self.keyPressed.emit(event)
        else:
            super(MyComboBox, self).keyPressEvent(event)

class MyListView(QtWidgets.QListView):
    keyPressed = QtCore.pyqtSignal(QtGui.QKeyEvent)

    def keyPressEvent(self, event):
        k = event.key()
        if k == 32 or k == 16777220:
            self.keyPressed.emit(event)
        else:
            super(MyListView, self).keyPressEvent(event)
