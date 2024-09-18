# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eqwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from mywidgets import CaptionWidget, MyLabel, MyCheckBox
from lang import tr

class Ui_eq_window(object):
    def setupUi(self, dialog_window):
        dialog_window.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        dialog_window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        dialog_window.setObjectName("Equalizer")
        dialog_window.resize(352, 188)
        dialog_window.setMinimumSize(QtCore.QSize(0, 120))
        dialog_window.setMaximumSize(QtCore.QSize(16777215, 220))
        dialog_window.setWindowTitle("Equalizer")
        self.dialoglayout = QtWidgets.QVBoxLayout(dialog_window)
        self.dialoglayout.setContentsMargins(14,14,14,14)
        self.dialoglayout.setSpacing(0)
        self.dialoglayout.setObjectName('dialoglayout')
        self.eq_window = QtWidgets.QWidget(dialog_window)
        self.eq_window.setObjectName('eq_window')
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setColor(QtGui.QColor(0, 0, 0, 255))
        effect.setOffset(0)
        effect.setBlurRadius(18)
        self.eq_window.setGraphicsEffect(effect)

        self.dialoglayout.addWidget(self.eq_window)

        self.eq_window.setStyleSheet("QWidget#eq_window {border-style: inset;border-width: 1px; border-color: #242424; border-radius: 10px; background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #222222, stop:0.5 #282a2b, stop:1 #222);}\n"
"QLabel {color: #ccc;}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.eq_window)
        self.verticalLayout.setContentsMargins(6, 2, 6, 6)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.w_close = QtWidgets.QWidget(self.eq_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_close.sizePolicy().hasHeightForWidth())
        self.w_close.setSizePolicy(sizePolicy)

        self.w_close.setStyleSheet("QWidget#w_close {background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #36000000 stop:1 #00000000);}")
        self.w_close.setObjectName("w_close")
        self.hl_top = QtWidgets.QHBoxLayout(self.w_close)
        self.hl_top.setContentsMargins(0, 1, 0, 1)
        self.hl_top.setSpacing(0)
        self.hl_top.setObjectName("hl_top")
        self.cbEnable = MyCheckBox(self.w_close)
        #self.cbEnable.setStyleSheet('QCheckBox {background: transparent; border-width: 0px;} QCheckBox::indicator {width: 18px; height: 18px;}'
        #'QCheckBox::indicator:unchecked {image: url(:/images/unchecked.png);} QCheckBox::indicator:checked {image: url(:/images/checked.png);}')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbEnable.sizePolicy().hasHeightForWidth())
        self.cbEnable.setSizePolicy(sizePolicy)
        self.cbEnable.setObjectName("cbEnable")
        self.hl_top.addWidget(self.cbEnable)

        self.l_caption = CaptionWidget(dialog_window, self.w_close)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.l_caption.setFont(font)

        #self.l_caption.setAlignment(QtCore.Qt.AlignCenter)
        self.l_caption.setObjectName("l_caption")
        self.hl_top.addWidget(self.l_caption)
        #spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.hl_top.addItem(spacerItem1)
        self.l_close = MyLabel({'default': 'QLabel {background: url(":/images/close.png") no-repeat center center } QLabel:hover {background:  url(":/images/close_h.png") no-repeat center center}'},self.w_close)
        self.l_close.setMinimumSize(QtCore.QSize(18, 18))
        self.l_close.setMaximumSize(QtCore.QSize(18, 18))
        self.l_close.setText("")
        self.l_close.setObjectName("l_close")
        self.hl_top.addWidget(self.l_close)
        self.verticalLayout.addWidget(self.w_close)
        self.w_bars = QtWidgets.QWidget(self.eq_window)
        self.w_bars.setMinimumSize(QtCore.QSize(0, 120))
        self.w_bars.setStyleSheet("QWidget#w_bars {\n"
"background: rgba(0, 0, 0, 60);\n"
"border-style: inset;\n"
"border-width: 1px;\n"
"border-color: #445;\n"
"border-radius: 10px;\n"
"}")
        self.w_bars.setObjectName("w_bars")
        self.verticalLayout.addWidget(self.w_bars)

        self.retranslateUi(dialog_window)
        QtCore.QMetaObject.connectSlotsByName(self.eq_window)

    def retranslateUi(self, dialog_window):
        self.l_caption.caption = tr("equalizer")

import images_rc
