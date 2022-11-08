# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eqwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from mywidgets import MELabel, MyLabel, MyCheckBox


class Ui_eq_window(object):
    def setupUi(self, eq_window):
        eq_window.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        eq_window.setObjectName("eq_window")
        eq_window.resize(324, 186)
        eq_window.setMinimumSize(QtCore.QSize(0, 192))
        eq_window.setMaximumSize(QtCore.QSize(16777215, 192))
        eq_window.setStyleSheet("QWidget#eq_window {background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #262638, stop:0.5 #50586b, stop:1 #223);}\n"
"QLabel {color: #ccc;}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(eq_window)
        self.verticalLayout.setContentsMargins(6, 2, 6, 6)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.w_close = QtWidgets.QWidget(eq_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_close.sizePolicy().hasHeightForWidth())
        self.w_close.setSizePolicy(sizePolicy)
        #self.w_close.setStyleSheet("QWidget#w_close {background: #20000000;}")
        self.w_close.setStyleSheet("QWidget#w_close {background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #36000000 stop:1 #00000000);}")
        self.w_close.setObjectName("w_close")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.w_close)
        self.horizontalLayout_3.setContentsMargins(0, 1, 0, 1)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cbEnable = MyCheckBox(self.w_close)
        #self.cbEnable.setStyleSheet('QCheckBox {background: transparent; border-width: 0px;} QCheckBox::indicator {width: 18px; height: 18px;}'
        #'QCheckBox::indicator:unchecked {image: url(:/images/unchecked.png);} QCheckBox::indicator:checked {image: url(:/images/checked.png);}')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbEnable.sizePolicy().hasHeightForWidth())
        self.cbEnable.setSizePolicy(sizePolicy)
        #self.cbEnable.setText("")
        self.cbEnable.setObjectName("cbEnable")
        self.horizontalLayout_3.addWidget(self.cbEnable)

        self.label_2 = MELabel(self.w_close)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        #spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.horizontalLayout_3.addItem(spacerItem1)
        self.l_addplaylist_2 = MyLabel(self.w_close)
        self.l_addplaylist_2.setMinimumSize(QtCore.QSize(18, 18))
        self.l_addplaylist_2.setMaximumSize(QtCore.QSize(18, 18))
        self.l_addplaylist_2.setStyleSheet("QLabel  {background:  url(\":/images/close.png\") }\n"
"QLabel:hover {background:  url(\":/images/close_h.png\")}")
        self.l_addplaylist_2.setText("")
        self.l_addplaylist_2.setObjectName("l_addplaylist_2")
        self.horizontalLayout_3.addWidget(self.l_addplaylist_2)
        self.verticalLayout.addWidget(self.w_close)
        self.widget = QtWidgets.QWidget(eq_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 1, 0, 1)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.cbPreset = QtWidgets.QComboBox(self.widget)
        self.cbPreset.setStyleSheet("QComboBox {\n"
"    background: rgba(0, 0, 0, 60);\n"
"    border-radius: 2px;\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-color: #445;\n"
"\n"
"};")
        self.cbPreset.setObjectName("cbPreset")
        self.horizontalLayout_2.addWidget(self.cbPreset)
        '''
        self.l_addpreset = MyLabel(self.widget)
        self.l_addpreset.setMinimumSize(QtCore.QSize(24, 24))
        self.l_addpreset.setMaximumSize(QtCore.QSize(24, 24))
        self.l_addpreset.setStyleSheet("QLabel  {background:  url(\":/images/add.png\") }\n"
"QLabel:hover {background:  url(\":/images/add_h.png\")}")
        self.l_addpreset.setText("")
        self.l_addpreset.setObjectName("l_addpreset")
        self.horizontalLayout_2.addWidget(self.l_addpreset)
        self.l_editpreset = QtWidgets.QLabel(self.widget)
        self.l_editpreset.setMinimumSize(QtCore.QSize(24, 24))
        self.l_editpreset.setMaximumSize(QtCore.QSize(24, 24))
        self.l_editpreset.setStyleSheet("QLabel  {background:  url(\":/images/edit.png\") }\n"
"QLabel:hover {background:  url(\":/images/edit_h.png\")}")
        self.l_editpreset.setText("")
        self.l_editpreset.setObjectName("l_editpreset")
        self.horizontalLayout_2.addWidget(self.l_editpreset)
        self.l_delpreset = QtWidgets.QLabel(self.widget)
        self.l_delpreset.setMinimumSize(QtCore.QSize(24, 24))
        self.l_delpreset.setMaximumSize(QtCore.QSize(24, 24))
        self.l_delpreset.setStyleSheet("QLabel  {background:  url(\":/images/del.png\") }\n"
"QLabel:hover {background:  url(\":/images/del_h.png\")}")
        self.l_delpreset.setText("")
        self.l_delpreset.setObjectName("l_delpreset")
        self.horizontalLayout_2.addWidget(self.l_delpreset)'''
        self.verticalLayout.addWidget(self.widget)
        self.w_bars = QtWidgets.QWidget(eq_window)
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

        self.retranslateUi(eq_window)
        QtCore.QMetaObject.connectSlotsByName(eq_window)

    def retranslateUi(self, eq_window):
        _translate = QtCore.QCoreApplication.translate
        eq_window.setWindowTitle(_translate("eq_window", "Form"))
        self.label_2.setText(_translate("eq_window", "- - Эквалайзер - -"))
        self.l_addplaylist_2.setToolTip(_translate("eq_window", "Добавить пресет"))
        self.label.setText(_translate("eq_window", "Пресеты:"))
        #self.l_addpreset.setToolTip(_translate("eq_window", "Добавить пресет"))
        #self.l_editpreset.setToolTip(_translate("eq_window", "Переименовать пресет"))
        #self.l_delpreset.setToolTip(_translate("eq_window", "Удалить пресет"))
import images_rc
