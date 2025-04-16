from PyQt5 import QtCore, QtGui, QtWidgets
from lang import tr
from mywidgets import CaptionWidget, MyLabel

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("EQSettingsDialog")
        Dialog.resize(280, 300)
        Dialog.setWindowTitle(tr("eq_settings_title"))
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        Dialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.dialoglayout = QtWidgets.QVBoxLayout(Dialog)
        self.dialoglayout.setContentsMargins(14, 14, 14, 14)
        self.dialoglayout.setSpacing(0)
        self.dialoglayout.setObjectName('dialoglayout')
        self.eq_settings_widget = QtWidgets.QWidget(Dialog)
        self.eq_settings_widget.setObjectName("eq_settings_widget")
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setColor(QtGui.QColor(0, 0, 0, 255))
        effect.setOffset(0)
        effect.setBlurRadius(18)
        self.eq_settings_widget.setGraphicsEffect(effect)

        self.dialoglayout.addWidget(self.eq_settings_widget)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.eq_settings_widget)
        self.verticalLayout.setContentsMargins(6, 2, 6, 6)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.w_close = QtWidgets.QWidget(self.eq_settings_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_close.sizePolicy().hasHeightForWidth())
        self.w_close.setSizePolicy(sizePolicy)

        self.w_close.setStyleSheet(
            "QWidget#w_close {background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #36000000 stop:1 #00000000);}")
        self.w_close.setObjectName("w_close")
        self.hl_top = QtWidgets.QHBoxLayout(self.w_close)
        self.hl_top.setContentsMargins(0, 1, 0, 1)
        self.hl_top.setSpacing(4)
        self.hl_top.setObjectName("hl_top")

        self.l_caption = CaptionWidget(Dialog, self.w_close)
        self.l_caption.caption = tr("eq_settings_title")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.l_caption.setFont(font)
        # self.l_caption.setAlignment(QtCore.Qt.AlignCenter)
        self.l_caption.setObjectName("l_caption")
        self.hl_top.addWidget(self.l_caption)
        self.l_close = MyLabel({'default': 'QLabel {background: url(":/images/close.png") no-repeat center center } '
                                           'QLabel:hover {background:  url(":/images/close_h.png") no-repeat center '
                                           'center}'}, self.w_close)
        self.l_close.setMinimumSize(QtCore.QSize(18, 18))
        self.l_close.setMaximumSize(QtCore.QSize(18, 18))
        self.l_close.setText("")
        self.l_close.setObjectName("l_close")
        self.hl_top.addWidget(self.l_close)
        self.verticalLayout.addWidget(self.w_close)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSpacing(4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.l_freq = QtWidgets.QLabel(self.eq_settings_widget)
        self.l_freq.setText(tr("center_frequency"))
        self.l_freq.setObjectName("l_freq")
        self.gridLayout.addWidget(self.l_freq, 0, 1, 1, 1)
        self.l_width = QtWidgets.QLabel(self.eq_settings_widget)
        self.l_width.setText(tr("band_width"))
        self.l_width.setObjectName("l_width")
        self.gridLayout.addWidget(self.l_width, 0, 2, 1, 1)
        self.grid_components = []
        self.validator = QtGui.QIntValidator(1, 19000)
        for i in range(10):
            l_num = QtWidgets.QLabel(self.eq_settings_widget)
            l_num.setText(f"{i+1}.")
            l_num.setObjectName(f"l_num_{i}")
            self.gridLayout.addWidget(l_num, i+1, 0, 1, 1)
            e_freq = QtWidgets.QLineEdit(self.eq_settings_widget)
            e_freq.setObjectName(f"e_freq_{i}")
            e_freq.setValidator(self.validator)
            self.gridLayout.addWidget(e_freq, i+1, 1, 1, 1)
            e_width = QtWidgets.QLineEdit(self.eq_settings_widget)
            e_width.setObjectName(f"e_width_{i}")
            e_width.setValidator(self.validator)
            self.gridLayout.addWidget(e_width, i+1, 2, 1, 1)
            self.grid_components.append((l_num, e_freq, e_width))

        self.horizontalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.eq_settings_widget)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        self.verticalLayout.addLayout(self.horizontalLayout)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

