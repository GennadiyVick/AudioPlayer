from PyQt5 import QtGui, QtCore,QtWidgets
import math

class VisWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(VisWidget,self).__init__(parent)
        self.fftbands = []
        self.peakvalues = []
        self.passedcounter = []
        self.updatebusy = 0
        self.zerofft = False


    def updatefft(self, fftbands, zerofft):
        if self.zerofft and zerofft:
            return
        self.zerofft = zerofft
        self.fftbands = fftbands
        if len(self.peakvalues) == 0:
            self.peakvalues = [0 for i in range(len(fftbands))]
            self.passedcounter = [0 for i in range(len(fftbands))]
        if self.updatebusy == 0: self.update()

    def paintEvent(self, event):
        if self.updatebusy > 0:
            return
        painter = QtGui.QPainter(self)
        #painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen()
        pen.setWidth(0)
        painter.setPen(pen)
        brush = QtGui.QBrush(QtGui.QColor(18,18,18))
        painter.setBrush(brush)
        painter.drawRoundedRect(0,0,self.width(),self.height(),8,8)
        #painter.setRenderHint(0)

        bcount = len(self.fftbands)
        if bcount == 0: return
        self.updatebusy += 1

        w = self.width()-10
        h = self.height()-10
        bandwidth = round(w / bcount)
        bandheight = h
        grad = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(0, h))
        grad.setColorAt(0, QtGui.QColor(255, 0, 0))
        grad.setColorAt(0.5, QtGui.QColor(255, 255, 0))
        grad.setColorAt(1, QtGui.QColor(0, 255, 0))
        brush = QtGui.QBrush(grad)
        painter.setBrush(brush)
        pen2 = QtGui.QPen(QtGui.QColor(132, 255, 255))
        pen2.setWidth(1)
        bw = round(bandwidth-1)

        for i in range(bcount):
            v = self.fftbands[i]
            if v > bandheight: v = bandheight
            if v > 0:
                x = round(i*bandwidth)
                y = bandheight-v
                r = QtCore.QRect(x+5,y+5,bw,h-y)
                painter.setPen(pen)
                painter.drawRect(r)
                #painter.fillRect(r, grad)


            if v >= int(self.peakvalues[i]):
                self.peakvalues[i] = v + 0.01  # 0.01 : to compensate round off
                self.passedcounter[i] = 0
            else:
                if int(self.peakvalues[i]) > 0:
                    painter.setPen(pen2)
                    y = round(bandheight-self.peakvalues[i])
                    x = round(i*bandwidth)
                    painter.drawLine(x+5,y+5,x+4+bw,y+5)

                    if self.passedcounter[i] >= 8:
                        self.peakvalues[i] = self.peakvalues[i] - 0.3 * (self.passedcounter[i] - 8)

                    if self.peakvalues[i] < 0:
                        self.peakvalues[i] = 0
                    else:
                        self.passedcounter[i]+=1
        painter.end()
        self.updatebusy -= 1
    


