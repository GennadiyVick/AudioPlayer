from PyQt5 import QtGui, QtCore,QtWidgets
from colorsys import hsv_to_rgb


def get_color_spectr():
    ''' get color spectr from red to blue '''
    side_percent = 9
    spectr_percent = 82
    color_spectr = []
    for i in range(side_percent):
        color_spectr.append(hsv_to_rgb(0, 1.0, int(128 + i * (128 / side_percent))))
    sp_bar = 0.73 / spectr_percent
    for i in range(spectr_percent):
        color_spectr.append(hsv_to_rgb(i * sp_bar, 1.0, 255))
    for i in range(side_percent):
        color_spectr.append(hsv_to_rgb(0.73, 1.0, int(255 - i * (128 / side_percent))))
    for i in range(100):
        color_spectr[i] = int(color_spectr[i][0]), int(color_spectr[i][1]), int(color_spectr[i][2])
    return color_spectr


class VisWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(VisWidget, self).__init__(parent)
        self.fftbands = []
        self.peakvalues = []
        self.passedcounter = []
        self.updatebusy = 0
        self.zerofft = False
        self.draw_type = 0
        self.bandcolors = []
        self.color_spectr = get_color_spectr()


    def update_colors(self):
        self.bandcolors = []
        bc = len(self.fftbands)
        for i in range(bc):
            cl = self.color_spectr[int(i * (100 / bc))]
            self.bandcolors.append(cl)

    def updatefft(self, fftbands, zerofft):
        if self.zerofft and zerofft:
            return
        self.zerofft = zerofft
        self.fftbands = fftbands
        if len(self.bandcolors) == 0:
            self.update_colors()
        if len(self.peakvalues) == 0:
            self.peakvalues = [0] * len(fftbands)
            self.passedcounter = [0] * len(fftbands)
        self.update()

    def draw_type_0(self, painter):
        pen = QtGui.QPen()
        pen.setWidth(0)
        bcount = len(self.fftbands)
        if bcount == 0: return
        self.updatebusy += 1

        w = self.width() - 10
        h = self.height() - 10
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
        bw = round(bandwidth - 1)

        for i in range(bcount):
            v = self.fftbands[i]
            if v > bandheight: v = bandheight
            if v > 0:
                x = round(i * bandwidth)
                y = bandheight - v
                r = QtCore.QRect(x + 5, y + 5, bw, h - y)
                painter.setPen(pen)
                painter.drawRect(r)
                # painter.fillRect(r, grad)

            if v >= int(self.peakvalues[i]):
                self.peakvalues[i] = v + 0.01  # 0.01 : to compensate round off
                self.passedcounter[i] = 0
            else:
                if int(self.peakvalues[i]) > 0:
                    painter.setPen(pen2)
                    y = round(bandheight - self.peakvalues[i])
                    x = round(i * bandwidth)
                    painter.drawLine(x + 5, y + 5, x + 4 + bw, y + 5)

                    if self.passedcounter[i] >= 8:
                        self.peakvalues[i] = self.peakvalues[i] - 0.3 * (self.passedcounter[i] - 8)

                    if self.peakvalues[i] < 0:
                        self.peakvalues[i] = 0
                    else:
                        self.passedcounter[i] += 1

    def draw_type_1(self, painter):
        w = self.width() - 10
        h = self.height() - 10

        bcount = len(self.fftbands)
        if bcount == 0: return
        self.updatebusy += 1

        # draw bands
        bandwidth = round(w / bcount)
        bw = bandwidth - 1
        block_height = 6
        bh = block_height - 1

        for i in range(bcount):
            brush = QtGui.QBrush(QtGui.QColor(*self.bandcolors[i]))
            painter.setBrush(brush)
            v = self.fftbands[i]
            if v > h: v = h
            if v > 0:
                x = round(i * bandwidth)
                bc = round(v / block_height)
                for j in range(bc):
                    y = h - j * block_height
                    r = QtCore.QRect(x + 5, y, bw, bh)
                    painter.drawRect(r)
    def paintEvent(self, event):
        if self.updatebusy > 0:
            return
        painter = QtGui.QPainter(self)

        pen = QtGui.QPen()
        pen.setWidth(0)
        painter.setPen(pen)

        # bg draw
        grad = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(self.width(), 0))
        grad.setColorAt(0, QtGui.QColor(12, 12, 14))
        grad.setColorAt(0.5, QtGui.QColor(18, 18, 33))
        grad.setColorAt(1, QtGui.QColor(12, 12, 14))
        brush = QtGui.QBrush(grad)
        painter.setBrush(brush)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 8, 8)

        if self.draw_type == 0:
            self.draw_type_0(painter)
        else:
            self.draw_type_1(painter)

        painter.end()
        self.updatebusy -= 1

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.draw_type += 1
            if self.draw_type > 1:
                self.draw_type = 0
    


