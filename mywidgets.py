from PySide6 import QtCore, QtWidgets, QtGui
import images_rc


class CaptionWidget(QtWidgets.QWidget):
    def __init__(self, movewindow, parent=None):
        super(CaptionWidget, self).__init__(parent)
        self.setMouseTracking(True)
        self.movewindow = movewindow
        self.mx = 0
        self.my = 0
        self.mousedown = False
        self.caption = ''

    def mousePressEvent(self, event):
        if self.movewindow is None:
            return
        if event.buttons() == QtCore.Qt.LeftButton:
            self.mx = event.globalX()
            self.my = event.globalY()
            self.l = self.movewindow.pos().x()
            self.t = self.movewindow.pos().y()
            self.mousedown = True

    def mouseReleaseEvent(self, event):
        self.mousedown = False

    def mouseMoveEvent(self, event):
        if self.mousedown:
            x = event.globalX()
            y = event.globalY()
            t = y - self.my + self.t
            l = x - self.mx + self.l
            self.movewindow.do_move(l, t)

    def paintEvent(self, event):
        if len(self.caption) == 0:
            super(CaptionWidget, self).paintEvent(event)
            return
        with QtGui.QPainter(self) as painter:
            painter.setPen(QtGui.QColor(220, 220, 255))
            painter.drawText(event.rect().adjusted(1, 1, 1, 1), QtCore.Qt.AlignCenter, self.caption)



class VerSizeWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(VerSizeWidget, self).__init__(parent)
        self.setMouseTracking(True)
        self.parent = parent
        self.mx = 0
        self.my = 0
        self.mousedown = False

    def mousePressEvent(self, event):
        if self.parent is None:
            return
        if event.buttons() == QtCore.Qt.LeftButton:
            self.mx = event.globalX()
            self.my = event.globalY()
            self.h = self.parent.parent().size().height()
            self.w = self.parent.parent().size().width()
            self.mousedown = True

    def mouseReleaseEvent(self, event):
        self.mousedown = False

    def mouseMoveEvent(self, event):
        if self.mousedown:
            x = event.globalX()
            y = event.globalY()
            h = y - self.my + self.h
            self.parent.parent().resize(QtCore.QSize(self.w, h))


class MouseWidget(QtWidgets.QLabel):
    onMousePress = QtCore.Signal(QtGui.QMouseEvent)
    onMouseRelease = QtCore.Signal(QtGui.QMouseEvent)
    onMouseMove = QtCore.Signal(QtGui.QMouseEvent)

    def __init__(self, parent=None):
        super(MouseWidget, self).__init__(parent)
        self.setMouseTracking(True)
        self.md = False
        self.setText('')

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.md = True
            self.onMousePress.emit(event)

    def mouseReleaseEvent(self, event):
        if self.md:
            self.md = False
            self.onMouseRelease.emit(event)

    def mouseMoveEvent(self, event):
        if self.md:
            self.onMouseMove.emit(event)


class MyLabel(QtWidgets.QLabel):
    onClick = QtCore.Signal()

    def __init__(self, styles, parent):
        super(MyLabel, self).__init__(parent)
        self.styles = styles if styles != None else {}
        self.checkable = False
        self.checked = False
        if 'default' in self.styles:
            self.setStyleSheet(self.styles['default'])
        self.leftbtn = False

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.leftbtn = True

            if 'pressed' in self.styles:
                self.setStyleSheet(self.styles['pressed'])
            self.raise_()
        else:
            self.leftbtn = False

    def mouseReleaseEvent(self, event):
        if self.leftbtn:
            self.leftbtn = False

            x, y = event.pos().x(), event.pos().y()
            if 0 < x < self.width() and 0 < y < self.height():
                self.onClick.emit()
                if self.checkable:
                    self.checked = not self.checked

            if self.checked and 'checked' in self.styles:
                self.setStyleSheet(self.styles['checked'])
            elif 'default' in self.styles:
                self.setStyleSheet(self.styles['default'])

    def updatestyle(self):
        style = ''
        if self.leftbtn:
            if 'pressed' in self.styles:
                style = self.styles['pressed']
        else:
            if self.checked and 'checked' in self.styles:
                style = self.styles['checked']
            elif 'default' in self.styles:
                style = self.styles['default']
        self.setStyleSheet(style)


class MyCheckBox(QtWidgets.QLabel):
    toggled = QtCore.Signal()

    def __init__(self, parent=None):
        super(MyCheckBox, self).__init__(parent)
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
    keyPressed = QtCore.Signal(QtGui.QKeyEvent)

    def keyPressEvent(self, event):
        if event.key() == 32:
            self.keyPressed.emit(event)
        else:
            super(MyComboBox, self).keyPressEvent(event)


class MyListView(QtWidgets.QListView):
    keyPressed = QtCore.Signal(QtGui.QKeyEvent)

    def __init__(self, parent):
        super(MyListView, self).__init__(parent)
        self.animations = []
        self.ani_timer = QtCore.QTimer(self)
        self.ani_timer.setInterval(35)
        self.ani_timer.timeout.connect(self.onTimer)
        self.scroll_down = False

    def onTimer(self):
        if len(self.animations) == 0:
            self.ani_timer.stop()
            return
        ani = self.animations[0]
        ani['value'] += ani['step']
        if ani['step'] < 0:
            if ani['value'] <= ani['end_value']:
                ani['value'] = ani['end_value']
                self.animations.pop(0)
        else:
            if ani['value'] >= ani['end_value']:
                ani['value'] = ani['end_value']
                self.animations.pop(0)
        self.verticalScrollBar().setValue(ani['value'])

    def keyPressEvent(self, event):
        k = event.key()
        if k == 32 or k == 16777220:
            self.keyPressed.emit(event)
        else:
            super(MyListView, self).keyPressEvent(event)

    def wheelEvent(self, e: QtGui.QWheelEvent):
        v = self.verticalScrollBar().value()
        if len(self.animations) > 0:
            v = self.animations[len(self.animations) - 1]['end_value']
        if e.pixelDelta().y() > 0:
            if v == 0: return
            if self.scroll_down and len(self.animations) > 0:
                self.animations.clear()
                v = self.verticalScrollBar().value()
            self.scroll_down = False
            ev = v - 40
            if ev < 0: ev = 0
            ani = {'value': v, 'step': -6, 'end_value': ev}
            self.animations.append(ani)
            if not self.ani_timer.isActive():
                self.ani_timer.start()
        else:
            if not self.scroll_down and len(self.animations) > 0:
                self.animations.clear()
                v = self.verticalScrollBar().value()
            self.scroll_down = True
            ev = v + 40
            if ev > self.verticalScrollBar().maximum():
                ev = self.verticalScrollBar().maximum()
            ani = {'value': v, 'step': 6, 'end_value': ev}
            self.animations.append(ani)
            if not self.ani_timer.isActive():
                self.ani_timer.start()


class ImageLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        super(ImageLabel, self).__init__(parent)
        self.pix = None
        self.setScaledContents(False)

    def setPixmap(self, pix):
        self.pix = pix
        super().setPixmap(self.scaledPixmap())

    def scaledPixmap(self):
        return self.pix.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

    def resizeEvent(self, event):
        if self.pix is not None:
            super().setPixmap(self.scaledPixmap())


class ImageWidget(QtWidgets.QWidget):
    def __init__(self, parent, size=None):
        super(ImageWidget,self).__init__(parent)
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.pix: QtGui.QPixmap = None
        self.wsize = size
        self.roundconners = 10

    def setPixmap(self, pixmap):
        if not pixmap:
            return
        self.pix = pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        #self.repaint()
        self.update()

    def get_pixmap(self):
        return self.pix

    def paintEvent(self, event):
        if self.pix is None: return
        with QtGui.QPainter(self) as painter:
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            brush = QtGui.QBrush(self.pix)
            painter.setBrush(brush)
            pen = QtGui.QPen()
            pen.setWidth(0)
            pen.setStyle(QtCore.Qt.NoPen)
            painter.setPen(pen)
            painter.drawRoundedRect(QtCore.QRect(0, 0, self.pix.width(), self.pix.height()), self.roundconners, self.roundconners)