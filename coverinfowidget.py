from PySide6 import QtCore, QtWidgets, QtGui
from mywidgets import ImageWidget


class CoverInfoWidget(QtWidgets.QWidget):
    """Виджет с обложкой и информацией c анимацией появления."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 180)

        # --- Виджет обложки ---
        self.l_image = ImageWidget(self)
        self.l_image.setObjectName("l_image")
        self.l_image.setMinimumSize(QtCore.QSize(180, 180))
        self.l_image.setMaximumSize(QtCore.QSize(180, 180))
        self.l_image.setPixmap(QtGui.QPixmap(":/images/logo.png"))

        # --- Виджет информации ---
        self.label_info = QtWidgets.QLabel(self)
        self.label_info.setWordWrap(True)
        self.label_info.setObjectName('label_info')
        self.label_info.setText(
            "<h2>Название Трека</h2>"
            "<p style='font-size: 10px; color: #aaa;'>Исполнитель</p>"
            "<p style='font-size: 10px;'>2023 • MP3 • 320kbps</p>"
        )
        self.label_info.move(180, 0)
        self.label_info.resize(120, 180)
        # Эффект прозрачности для текста
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self.label_info)
        self.label_info.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)
        # Анимация движения обложки
        self.anim_cover = QtCore.QPropertyAnimation(self.l_image, b"pos")
        self.anim_cover.setDuration(800)
        #self.anim_cover.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.anim_cover.finished.connect(self.anim_cover_finished)
        # Анимация эффекта прозрачности
        self.anim_info_opacity = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_info_opacity.setDuration(800)
        self.anim_info_opacity.setStartValue(0.0)
        self.anim_info_opacity.setEndValue(1.0)
        cover_x = (self.width() - 180) // 2
        self.l_image.move(cover_x, 0)
        self.anim_cover.setStartValue(QtCore.QPoint(cover_x, 0))
        self.anim_cover.setEndValue(QtCore.QPoint(0, 0))

    def load_mp3_data(self, pixmap, data=''):
        if data:
            self.label_info.setText(data)
        self.l_image.setPixmap(pixmap)
        self.opacity_effect.setOpacity(0.0)
        cover_x = (self.width() - 180) // 2
        self.l_image.move(cover_x, 0)
        self.l_image.show()
        if data:
            QtCore.QTimer.singleShot(1300, self._start_animation_sequence)

    def anim_cover_finished(self):
        self.anim_cover.stop()
        self.anim_info_opacity.start()

    def _start_animation_sequence(self):
        self.opacity_effect.setOpacity(0.0)
        self.anim_cover.start()
