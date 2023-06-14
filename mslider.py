from PyQt5 import QtGui, QtCore,QtWidgets
import images_rc

class MSlider(QtWidgets.QWidget):
    posChanged = QtCore.pyqtSignal(int)
    #timeChanged = QtCore.pyqtSignal(str)
    def __init__(self, parent = None):
        super(MSlider,self).__init__(parent)
        self.maxpos = 1000
        self.pos = 0
        self.images = []
        self.fgLeftImgIndex = -1
        self.fgCenterImgIndex = -1
        self.fgRightImgIndex = -1
        self.fitHeight = False
        self.leftMousePressed = False
        self.setImages(':/images/tb_fg_l.png',':/images/tb_fg_c.png',':/images/tb_fg_r.png')

    #public slots...
    def posChange(self, pos):
        if self.leftMousePressed: return
        if pos < 0: pos = 0
        self.pos = pos
        self.update()
        #self.timeChanged.emit(self.getCurTime())

    def maxChange(self, value):
        self.maxpos = value
        self.update()
        #self.timeChanged.emit(self.getCurTime())


    #public...
    def setImages(self, leftImg, centerImg, rightImg):
        if len(self.images) > 0:
            self.images.clear()
        self.images.append(QtGui.QPixmap(leftImg))
        self.images.append(QtGui.QPixmap(centerImg))
        self.images.append(QtGui.QPixmap(rightImg))
        self.update()

    #private...
    def imginRange(self, value):
        pass
    def getCurTime(self):
        pass

    #events...
    def mousePressEvent(self, event):
        self.leftMousePressed = event.buttons() == QtCore.Qt.LeftButton

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            w = self.width()
            x = event.x()
            if x < 0: x = 0
            if x > w: x = w
            self.pos = round(self.maxpos * (x/w))
            self.update()
    
    def mouseReleaseEvent(self, event):
        if self.leftMousePressed:
            w = self.width()
            x = event.x()
            if x < 0: x = 0
            if x > w: x = w
            self.pos = round(self.maxpos * (x/w))
            self.update()
            self.posChanged.emit(self.pos)
            self.leftMousePressed = False

    def paintEvent(self, event):
        if len(self.images) < 3:
            super(MSlider, self).paintEvent(event)
            return
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        #painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        ww = self.width()
        wh = self.height()
        p = round(ww*(self.pos/self.maxpos))
        fgSL = QtCore.QSize(self.images[0].width(),self.images[0].height())
        fgSC = QtCore.QSize(self.images[1].width(),self.images[1].height())
        fgSR = QtCore.QSize(self.images[2].width(),self.images[2].height())
        if self.fitHeight:
            fgSL.setWidth(self.images[0].width())
            fgSL.setHeight(wh)
            fgSC.setWidth(self.images[1].width())
            fgSC.setHeight(wh)
            fgSR.setWidth(self.images[2].width())
            fgSR.setHeight(wh)

        x = 0;
        y = 0;
        if not self.fitHeight:
            y = (wh - fgSL.height()) // 2
        if p < fgSL.width():
            if p == 0: return
            painter.drawPixmap(QtCore.QRect(x,y,p,fgSL.height()),self.images[0],QtCore.QRect(0,0,p,self.images[0].height()))
        else:
            painter.drawPixmap(QtCore.QRect(x,y,fgSL.width(),fgSL.height()),self.images[0])

        x = fgSL.width()
        if not self.fitHeight:
            y = (wh - fgSC.height()) // 2
        else:
            y = 0
        cw = ww-fgSL.width()-fgSR.width()
        if p < cw+fgSL.width():
            cw = p-fgSL.width()

        if cw > 0:
            painter.drawPixmap(QtCore.QRect(x,y,cw,fgSC.height()),self.images[1],QtCore.QRect(0,0,fgSC.width(),self.images[1].height()))
        x = ww-fgSR.width()
        if not self.fitHeight:
            y = (wh - fgSR.height()) // 2
        else: y = 0
        if p <= ww-fgSR.width():
            pass
        elif p == ww:
            painter.drawPixmap(QtCore.QRect(x,y,fgSR.width(),fgSR.height()),self.images[2])
        else:
            cw = fgSR.width() - (ww-p)
            painter.drawPixmap(QtCore.QRect(x,y,cw,fgSR.height()),self.images[2],QtCore.QRect(0,0,cw,self.images[2].height()))
        painter.end()

    def resizeEvent(self, event):
        self.update()
        #super().resizeEvent(event)


