from PySide6 import QtGui, QtCore,QtWidgets
import math


class MVolume(QtWidgets.QWidget):
    posChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(MVolume, self).__init__(parent)
        self.pi = 3.1415926535
        self.piGr = self.pi / 180
        self.knob = None
        self.bg = None
        self.updatebusy = 0
        self.busy = False
        self.currentAngle = 0
        self.maxangle = 270
        self.startangle = 224;
        self.gradientangle = self.startangle + 13
        self.linewidth = 2
        self.maxpos = 100
        self.position = 0
        self.fitBgImage = False
        self.borderBgOffset = 0
        self.oldAngle = 0.0
        self.color_gradient = [QtGui.QColor(0, 255, 255), QtGui.QColor(0, 0, 255)]

    #public...

    def getLineWidth(self):
        return self.linewidth

    def setLineWidth(self, value):
        self.linewidth = value
        if self.updatebusy == 0: self.update()

    def setMaxAngle(self, value):
        self.maxangle = value
        if self.updatebusy == 0: self.update()

    def getMaxAngle(self):
        return self.maxangle

    def setStartAngle(self, value):
        self.startangle = value
        if self.updatebusy == 0: self.update()

    def getStartAngle(self):
        return self.startangle

    def setKnobImage(self, img):
        self.knob = img
        if self.updatebusy == 0: self.update()

    def setKnobBgImage(self, img):
        self.bg = img
        if self.updatebusy == 0: self.update()

    def beginUpdate(self):
        self.updatebusy += 1

    def endUpdate(self):
        self.updatebusy -= 1
        if self.updatebusy == 0: self.update()
        if self.updatebusy < 0: self.updatebusy = 0

    # slots
    def setMax(self, value):
        self.maxpos = value;
        if self.position > self.maxpos:
            self.position = self.maxpos
        self.posToAngle()
        if self.updatebusy == 0: self.update()

    def setPos(self, value):
        if self.busy: return
        if value > self.maxpos:
            value = self.maxpos
        elif value < 0:
            value = 0
        self.position = value
        self.posToAngle()
        if self.updatebusy == 0: self.update()

    # private...
    def getAngle(self, la, na):
        a = na - la
        if la > na: a = la - na
        if 360 - a < a:
            if la > na:
                a = 360 - a
            else:
                a = a - 360
        elif la > na:
            a = -a
        return a

    def angleFromXY(self, x, y):
        px = x - self.width() // 2
        py = y - self.height() // 2
        return math.atan2(px,py) / self.piGr;

    def AngleToPos(self):
        if self.maxangle == 0: return 0
        k = self.currentAngle / self.maxangle
        return round(self.maxpos * k)

    def posToAngle(self):
        if self.maxpos == 0:
            self.currentAngle = 0
            return
        k = self.position / self.maxpos
        self.currentAngle = round(self.maxangle * k)

    #events...

    def paintEvent(self, event):
        with QtGui.QPainter(self) as painter:
            w = self.width()
            h = self.height()
            if self.bg is not None:
                x = (w - self.bg.width()) // 2
                y = (h - self.bg.height()) // 2
                painter.drawPixmap(QtCore.QRect(x, y, self.bg.width(), self.bg.height()), self.bg)

            x, y = 1, 1
            w -= 2
            h -= 2
            drawing_rect = QtCore.QRect(x, y, w, h)
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
            gradient = QtGui.QConicalGradient()
            gradient.setCenter(drawing_rect.center())
            gradient.setAngle(self.gradientangle)
            l = len(self.color_gradient)-1
            for i, color in enumerate(self.color_gradient):
                gradient.setColorAt(i/l, color)

            pen = QtGui.QPen(QtGui.QBrush(gradient), self.linewidth)
            pen.setCapStyle(QtCore.Qt.RoundCap)
            painter.setPen(pen)
            painter.drawArc(drawing_rect, int(self.startangle * 16), int(-self.currentAngle * 16))
            if self.knob is not None:
                x = (w - self.knob.width()) // 2
                y = (h - self.knob.height()) // 2
                ox = self.width() // 2
                oy = self.height() // 2
                painter.translate(ox, oy)
                painter.rotate(self.currentAngle-135)
                painter.translate(-ox, -oy)
                painter.drawPixmap(QtCore.QRect(x, y, self.knob.width(), self.knob.height()), self.knob)

    def resizeEvent(self, event):
        self.update()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.busy = True
            self.oldAngle = self.angleFromXY(event.x(),event.y())
            if self.oldAngle < 0:
                self.oldAngle = 360.0 + self.oldAngle

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            ra = self.angleFromXY(event.x(), event.y())
            newAngle = ra
            if ra < 0: newAngle = newAngle + 360.0
            a = self.getAngle(self.oldAngle, newAngle)
            self.currentAngle += -a
            self.oldAngle = newAngle
            if self.currentAngle < 0: self.currentAngle = 0
            if self.currentAngle > self.maxangle:
                self.currentAngle = self.maxangle
            self.update()
            p = self.AngleToPos()
            if p != self.position:
                self.position = p
                self.posChanged.emit(self.position)

    def mouseReleaseEvent(self, event):
        p = self.AngleToPos()
        if p != self.position:
            self.position = p
            self.posChanged.emit(self.position)
        self.busy = False

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.setPos(self.position+5)
        else:
            self.setPos(self.position-5)
        self.posChanged.emit(self.position)

