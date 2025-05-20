from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
from mvolume import MVolume


def create_button(name, left_pos, parent, event):
    btn = QPushButton(parent)
    btn.setText('')
    btn.setObjectName(name)
    btn.setFlat(True)
    btn.setGeometry(QtCore.QRect(left_pos, 0, 60, 45))
    btn.setFocusPolicy(Qt.NoFocus)
    btn.clicked.connect(event)
    return btn


class TrayPanelWidget(QWidget):
    play_click = pyqtSignal()
    pause_click = pyqtSignal()
    stop_click = pyqtSignal()
    prev_click = pyqtSignal()
    next_click = pyqtSignal()
    volume_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Устанавливаем размеры
        self.resize(272, 45)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.buttons_container = QWidget(self)
        self.buttons_container.setObjectName('wButtonContainer')
        self.buttons_container.setMinimumSize(QtCore.QSize(269, 45))
        self.buttons_container.setMaximumSize(QtCore.QSize(269, 45))

        # Добавляем кнопки
        self.prev_button  = create_button('bPrev', -1, self.buttons_container, self.on_prev_clicked)
        self.play_button  = create_button('bPlay', 41, self.buttons_container, self.on_play_clicked)
        self.pause_button = create_button('bPause',83, self.buttons_container, self.on_pause_clicked)
        self.stop_button  = create_button('bStop', 125, self.buttons_container, self.on_stop_clicked)
        self.next_button  = create_button('bNext', 167, self.buttons_container, self.on_next_clicked)
        self.create_volume_control()

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

    def create_volume_control(self):
        self.vol = MVolume(self.buttons_container)
        self.vol.resize(38, 38)
        self.vol.move(225, 6)
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
