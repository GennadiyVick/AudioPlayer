from PySide6 import QtCore, QtWidgets, QtGui
from mywidgets import MouseWidget


class EqSlider(QtWidgets.QWidget):
    posChange = QtCore.Signal(QtWidgets.QWidget, int)
    posChanged = QtCore.Signal(QtWidgets.QWidget, int)

    def __init__(self, parent=None, curpos=-1, maxpos=100):
        super(EqSlider, self).__init__(parent)
        # self.setStyleSheet("QWidget {background: url(\":/images/slider_bg.png\");}")
        self.ww = 30
        self.wh = 110
        self.bg_offset = 5
        self.setMinimumSize(QtCore.QSize(self.ww, self.wh))
        self.setMaximumSize(QtCore.QSize(self.ww, self.wh))
        self.maxpos = maxpos
        self.p_bg = QtGui.QPixmap(":/images/slider_bg.png")
        self.p_line = QtGui.QPixmap(":/images/eq_line.png")
        self.p_line_xoffset = (30 - self.p_line.width()) / 2
        self.knob = MouseWidget(self)
        self.knob.setMinimumSize(QtCore.QSize(22, 18))
        self.knob.setMaximumSize(QtCore.QSize(22, 18))
        self.knob.setStyleSheet('MouseWidget {background: #f0f;}')
        # self.knob.setStyleSheet('background: url(":/images/slider_knob.png")')
        self.knob.setStyleSheet("QLabel {background: url(\":/images/slider_knob.png\")}\n"
                                "QLabel:hover {background: url(\":/images/slider_knob_h.png\")}")
        self.knob_left = (self.ww - self.knob.width()) / 2
        self.knob_topoffset = self.knob.height() / 2
        self.knob.onMousePress.connect(self.knobMousePress)
        self.knob.onMouseMove.connect(self.knobMouseMove)
        self.knob.onMouseRelease.connect(self.knobMouseRelease)
        self.my = 0
        self.py = 0
        if curpos >= 0:
            self.setPos(curpos)
        else:
            self.setPos(50)
        # self.label_2.setObjectName("label_2")

    # Events...

    def paintEvent(self, event):
        with QtGui.QPainter(self) as painter:
            if self.p_bg is not None:
                painter.drawPixmap(QtCore.QRect(0, self.bg_offset, self.p_bg.width(), self.p_bg.height()), self.p_bg)
            if self.p_line is not None:
                ofs = 4  # self.bg_offset + 3
                h = self.wh - ofs * 2
                y = self.knob.pos().y() + self.knob_topoffset
                h = h - y
                r = QtCore.QRect(int(self.p_line_xoffset), int(y), int(self.p_line.width()), int(h))
                painter.drawPixmap(r, self.p_line)

    # private slots...

    def knobMousePress(self, event):
        self.my = event.globalPos().y()
        self.py = self.knob.pos().y()

    def knobMouseRelease(self, event):
        h = (self.wh - 18)
        k = (h - self.knob.pos().y()) / h
        self.setPos(round(k * self.maxpos))
        self.posChanged.emit(self, self.pos)

    def knobMouseMove(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            y = self.py + (event.globalPos().y() - self.my)
            h = self.wh - 18
            if y < 0:
                y = 0
            elif y > h:
                y = h
            p = round((h - y) / h * self.maxpos)
            self.knob.move(int(self.knob_left), int(y))
            if p != self.pos:
                self.pos = p
                self.posChange.emit(self, self.pos)

    # public slots...
    def setPos(self, pos):
        self.pos = pos
        h = self.wh - 18
        y = h - self.pos / self.maxpos * h
        self.knob.move(int(self.knob_left), int(y))
        self.update()

    def setMax(self, maxpos):
        self.maxpos = maxpos
        if self.pos > self.maxpos:
            self.pos = self.maxpos
        self.setPos(self.pos)
