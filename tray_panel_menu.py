from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, Signal, QPropertyAnimation
from PySide6 import QtCore, QtGui
from mvolume import MVolume


class LevelWidget(QWidget):
    def __init__(self, parent):
        super(LevelWidget, self).__init__(parent)
        self.level = 0

    def set_level(self, level):
        l = int(level * 100) if level < 0.5 else 50
        self.level = l / 50
        self.repaint()

    def paintEvent(self, event):
        with QtGui.QPainter(self) as painter:
            painter.fillRect(0, 0, self.width(), self.height(), QtGui.QColor(0, 0, 0, 0))
            #painter.fillRect(0, 0, self.width(), self.height(), QtGui.QColor(255, 0, 0))
            if self.level > 0:
                bar_width = int(self.width() * self.level)
                color = QtGui.QColor(0, 200, 255)  # Зелёный цвет
                painter.fillRect(0, 0, bar_width, self.height(), color)


def create_button(name, left_pos, parent, event):
    btn = QPushButton(parent)
    btn.setText('')
    btn.setObjectName(name)
    btn.setFlat(True)
    btn.setGeometry(QtCore.QRect(left_pos, 3, 60, 45))
    btn.setFocusPolicy(Qt.NoFocus)
    btn.clicked.connect(event)
    return btn


class TrayPanelWidget(QWidget):
    play_click = Signal()
    pause_click = Signal()
    stop_click = Signal()
    prev_click = Signal()
    next_click = Signal()
    volume_changed = Signal(int)

    def __init__(self, parent=None, player=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.player = player
        self.resize(272, 49)
        self.central_layout = QVBoxLayout(self)
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        #self.level_widget.move(4, 2)
        self.buttons_container = QWidget(self)
        #self.buttons_container.move(0, 4)
        #self.buttons_container.resize(269, 45)
        self.buttons_container.setObjectName('wButtonContainer')
        self.level_widget = LevelWidget(self.buttons_container) #QWidget(self.buttons_container)
        self.level_widget.resize(256, 2)
        self.level_widget.move(8, 4)

        # Добавляем кнопки
        self.prev_button = create_button('bPrev', -1, self.buttons_container, self.on_prev_clicked)
        self.play_button = create_button('bPlay', 41, self.buttons_container, self.on_play_clicked)
        self.pause_button = create_button('bPause',83, self.buttons_container, self.on_pause_clicked)
        self.stop_button = create_button('bStop', 125, self.buttons_container, self.on_stop_clicked)
        self.next_button = create_button('bNext', 167, self.buttons_container, self.on_next_clicked)
        self.create_volume_control()
        self.central_layout.addWidget(self.buttons_container)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self.opacity_effect)

        self.animation = QPropertyAnimation()
        self.animation.setTargetObject(self.opacity_effect)
        self.animation.setPropertyName(b'opacity')
        self.animation.setDuration(600)  # Продолжительность анимации в миллисекундах
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.finished.connect(self.do_close)
        self.fft_timer = QtCore.QTimer(self)
        self.fft_timer.setInterval(50)
        self.fft_timer.timeout.connect(self.fft_timer_timeout)
        self.fft_timer.start()

    def fft_timer_timeout(self):
        if self.isVisible() and self.player is not None:
            fft = self.player.get_mini_fftdata()
            if fft is None:
                if self.level_widget.level != 0:
                    self.level_widget.set_level(0)
            else:
                self.level_widget.set_level(fft)

    def create_volume_control(self):
        self.vol = MVolume(self.buttons_container)
        self.vol.resize(38, 38)
        self.vol.move(225, 8)
        self.vol.beginUpdate()
        self.vol.setKnobBgImage(QtGui.QPixmap(":/images/small_knob_bg.png"))
        self.vol.setKnobImage(QtGui.QPixmap(":/images/small_knob_ind.png"))
        self.vol.setPos(100)
        self.vol.endUpdate()
        self.vol.posChanged.connect(self.volume_changed_slot)

    def volume_changed_slot(self, volume):
        self.volume_changed.emit(volume)

    def do_close(self):
        if self.opacity_effect.opacity() < 0.02:
            self.close()
        else:
            self.setFocus()

    def on_play_clicked(self):
        self.play_click.emit()

    def on_pause_clicked(self):
        self.pause_click.emit()

    def on_next_clicked(self):
        self.next_click.emit()

    def on_prev_clicked(self):
        self.prev_click.emit()

    def on_stop_clicked(self):
        self.stop_click.emit()

    def showEvent(self, event):
        super().showEvent(event)
        self.activateWindow()
        self.setFocus()
        self.opacity_effect.setOpacity(0.0)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(500)
        self.animation.start()

    def hide_panel(self):
        self.animation.setDuration(300)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()

    def focusOutEvent(self, event):
        self.hide_panel()
