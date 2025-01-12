from PyQt5 import QtGui, QtCore,QtWidgets
from colorsys import hsv_to_rgb
from BASSPlayer import NumFFTBands


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


class Drawer:
    def __init__(self, widget):
        self.widget = widget

    def draw(self, painter: QtGui.QPainter, fftbands):
        pass


class DrawerGradient(Drawer):
    def __init__(self, widget):
        super(DrawerGradient, self).__init__(widget)
        self.pen0 = QtGui.QPen()
        self.pen0.setWidth(0)
        self.pen0.setStyle(QtCore.Qt.NoPen)
        self.bandcolors = []
        color_spectr = get_color_spectr()
        for i in range(NumFFTBands):
            cl = color_spectr[int(i * (100 / NumFFTBands))]
            self.bandcolors.append(cl)

    def draw(self, painter: QtGui.QPainter, fftbands):
        bcount = len(fftbands)
        if bcount == 0: return
        w = self.widget.width() - 10
        h = self.widget.height() - 10
        self.widget.updatebusy += 1
        painter.setPen(self.pen0)
        # draw bands
        bandwidth = round(w / bcount)
        bw = bandwidth - 1
        block_height = 6
        bh = block_height - 1
        try:
            for i in range(bcount):
                brush = QtGui.QBrush(QtGui.QColor(*self.bandcolors[i]))
                painter.setBrush(brush)
                v = fftbands[i]
                if v > h: v = h
                if v > 0:
                    x = round(i * bandwidth)
                    bc = v // block_height
                    lc = v / block_height - bc
                    if lc > 0: bc += 1
                    for j in range(bc):
                        y = h - j * block_height
                        r = QtCore.QRect(x + 5, y, bw-1, bh)
                        if j == bc - 1 and lc > 0:
                            brush = QtGui.QBrush(QtGui.QColor(*self.bandcolors[i], int(lc * 255)))
                            painter.setBrush(brush)
                        painter.drawRect(r)
        except Exception as e:
            print('viswidget paint error:', str(e))


class DrawerWinamp(Drawer):
    def __init__(self, widget):
        super(DrawerWinamp, self).__init__(widget)
        self.pen0 = QtGui.QPen()
        self.pen0.setWidth(0)
        self.gradient = None
        self.g_h = 0
        self.brush_grad = None
        self.pen1 = QtGui.QPen(QtGui.QColor(132, 255, 255))
        self.pen1.setWidth(1)
        self.peakvalues = [0] * NumFFTBands
        self.passedcounter = [0] * NumFFTBands

    def draw(self, painter: QtGui.QPainter, fftbands):
        bcount = len(fftbands)
        if bcount == 0: return
        self.widget.updatebusy += 1
        w = self.widget.width() - 10
        h = self.widget.height() - 10
        bandwidth = round(w / bcount)
        bandheight = h
        if self.gradient is None or h != self.g_h:
            self.g_h = h
            self.gradient = QtGui.QLinearGradient(QtCore.QPointF(0, 0), QtCore.QPointF(0, h))
            self.gradient.setColorAt(0, QtGui.QColor(255, 0, 0))
            self.gradient.setColorAt(0.5, QtGui.QColor(255, 255, 0))
            self.gradient.setColorAt(1, QtGui.QColor(0, 255, 0))
            self.brush_grad = QtGui.QBrush(self.gradient)

        painter.setBrush(self.brush_grad)
        bw = round(bandwidth - 1)
        try:
            for i in range(bcount):
                v = fftbands[i]
                if v > bandheight:
                    v = bandheight
                if v > 0:
                    x = round(i * bandwidth)
                    y = bandheight - v
                    r = QtCore.QRect(x + 5, y + 5, bw, h - y)
                    painter.setPen(self.pen0)
                    painter.drawRect(r)

                if v >= int(self.peakvalues[i]):
                    self.peakvalues[i] = v + 0.01  # 0.01 : to compensate round off
                    self.passedcounter[i] = 0
                else:
                    if int(self.peakvalues[i]) > 0:
                        painter.setPen(self.pen1)
                        y = round(bandheight - self.peakvalues[i])
                        x = round(i * bandwidth)
                        painter.drawLine(x + 5, y + 5, x + 4 + bw, y + 5)

                        if self.passedcounter[i] >= 8:
                            self.peakvalues[i] = self.peakvalues[i] - 0.3 * (self.passedcounter[i] - 8)

                        if self.peakvalues[i] < 0:
                            self.peakvalues[i] = 0
                        else:
                            self.passedcounter[i] += 1
        except Exception as e:
            print('viswidget paint error:', str(e))


class VisWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(VisWidget, self).__init__(parent)
        self.fftbands = []
        self.drawer_winamp = DrawerWinamp(self)
        self.drawer_gradient = DrawerGradient(self)
        self.updatebusy = 0
        self.zerofft = False
        self.draw_type = 0
        self.bandcolors = []
        self.color_spectr = get_color_spectr()

    def updatefft(self, fftbands, zerofft):
        self.fftbands = fftbands
        if zerofft and self.zerofft == zerofft:
            return
        if zerofft:
            if self.draw_type == 0:
                if all(v < 1 for v in self.drawer_winamp.peakvalues):
                    self.zerofft = zerofft
                    self.update()
                    #self.repaint()
                    return
            else:
                self.zerofft = zerofft
                self.update()
                #self.repaint()
                return
        else:
            self.zerofft = zerofft
        #self.update()
        self.repaint()

    def paintEvent(self, event):
        if self.updatebusy > 0:
            return
        painter = QtGui.QPainter(self)
        if self.draw_type == 0:
            self.drawer_winamp.draw(painter, self.fftbands)
        else:
            self.drawer_gradient.draw(painter, self.fftbands)

        painter.end()
        self.updatebusy -= 1
        if self.updatebusy < 0:
            self.updatebusy = 0

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.draw_type += 1
            if self.draw_type > 1:
                self.draw_type = 0
    


