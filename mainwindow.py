
from PyQt5 import QtCore, QtGui, QtWidgets
from mywidgets import MyLabel, MyComboBox, MyListView


#вместо кнопок я использую MyLabel, смотрится лучше и фокус на себя не берут.
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(302, 354)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet('''QWidget {background: #262638; color: #aaa;}
QWidget#centralwidget {background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #262638, stop:0.5 #50586b, stop:1 #223);}
QScrollBar {border-radius: 5px;}
QScrollBar:vertical {border-radius: 5px; width: 10px;}
QScrollBar:horizontal {border-top: 1px solid #1c1c1c; height: 10px; }
QScrollBar::handle {margin: -1px; background: #446; border: 1px solid #1c1c1c;}
QScrollBar::handle:vertical {min-height: 10px;}
QScrollBar::handle:horizontal {min-width: 10px;}
QScrollBar::handle:hover {background: #4ab;}
QScrollBar::left-arrow, QScrollBar::right-arrow, QScrollBar::up-arrow,
QScrollBar::down-arrow, QScrollBar::sub-line, QScrollBar::add-line,
QScrollBar::add-page, QScrollBar::sub-page {
  background: #2e2e3e; height: 0; width: 0; border-radius: 0; border: 0;}''')
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.w_info = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_info.sizePolicy().hasHeightForWidth())
        self.w_info.setSizePolicy(sizePolicy)
        self.w_info.setMinimumSize(QtCore.QSize(0, 52))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.w_info.setFont(font)
        self.w_info.setStyleSheet("QWidget {\n"
"    background: transparent;\n"
"}\n"
"QWidget#w_info {\n"
"background: rgba(0, 0, 0, 60);\n"
"border-style: inset;\n"
"border-width: 1px;\n"
"border-color: #445;\n"
"border-radius: 10px;\n"
"}")
        self.w_info.setObjectName("w_info")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.w_info)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_3 = QtWidgets.QWidget(self.w_info)
        self.widget_3.setStyleSheet("")
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.state_icon = QtWidgets.QLabel(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.state_icon.sizePolicy().hasHeightForWidth())
        self.state_icon.setSizePolicy(sizePolicy)
        self.state_icon.setMinimumSize(QtCore.QSize(20, 0))
        self.state_icon.setMaximumSize(QtCore.QSize(20, 20))
        self.state_icon.setStyleSheet("background: transparent;\n"
"border-width: 0px;\n"
"border-radius: 0px;")
        self.state_icon.setText("")
        self.state_icon.setPixmap(QtGui.QPixmap(":/images/stop_state.png"))
        self.state_icon.setScaledContents(True)
        self.state_icon.setObjectName("state_icon")
        self.horizontalLayout.addWidget(self.state_icon)
        self.l_info = QtWidgets.QLabel(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_info.sizePolicy().hasHeightForWidth())
        self.l_info.setSizePolicy(sizePolicy)
        self.l_info.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.l_info.setFont(font)
        self.l_info.setStyleSheet("")
        self.l_info.setText("")
        self.l_info.setWordWrap(True)
        self.l_info.setObjectName("l_info")
        self.horizontalLayout.addWidget(self.l_info)
        self.verticalLayout.addWidget(self.widget_3)
        self.l_time = QtWidgets.QLabel(self.w_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_time.sizePolicy().hasHeightForWidth())
        self.l_time.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.l_time.setFont(font)
        self.l_time.setStyleSheet("padding-left: 20px;")
        self.l_time.setObjectName("l_time")
        self.verticalLayout.addWidget(self.l_time)
        self.verticalLayout_2.addWidget(self.w_info)
        self.w_track = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_track.sizePolicy().hasHeightForWidth())
        self.w_track.setSizePolicy(sizePolicy)
        self.w_track.setMinimumSize(QtCore.QSize(0, 16))
        self.w_track.setStyleSheet("QWidget#w_track {\n"
"    background: rgba(0, 0, 0, 60);\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-color: #445;\n"
"    border-radius: 7px\n"
"};")
        self.w_track.setObjectName("w_track")
        self.verticalLayout_2.addWidget(self.w_track)
        self.w_controls = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_controls.sizePolicy().hasHeightForWidth())
        self.w_controls.setSizePolicy(sizePolicy)
        self.w_controls.setMinimumSize(QtCore.QSize(0, 50))
        self.w_controls.setStyleSheet("background:transparent")
        self.w_controls.setObjectName("w_controls")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.w_controls)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_panel = QtWidgets.QWidget(self.w_controls)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_panel.sizePolicy().hasHeightForWidth())
        self.btn_panel.setSizePolicy(sizePolicy)
        self.btn_panel.setStyleSheet("")
        self.btn_panel.setObjectName("btn_panel")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.btn_panel)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.wButtonContainer = QtWidgets.QWidget(self.btn_panel)
        self.wButtonContainer.setMinimumSize(QtCore.QSize(156, 32))
        self.wButtonContainer.setMaximumSize(QtCore.QSize(156, 32))
        self.wButtonContainer.setObjectName("wButtonContainer")
        self.lPref = MyLabel(self.wButtonContainer)
        self.lPref.setGeometry(QtCore.QRect(0, 0, 44, 32))
        self.lPref.setMinimumSize(QtCore.QSize(44, 32))
        self.lPref.setMaximumSize(QtCore.QSize(44, 32))
        self.lPref.setStyleSheet("QLabel  {background:  url(\":/images/prev_btn.png\") }\n"
"QLabel:hover {background:  url(\":/images/prev_btn_pressed.png\")}")
        self.lPref.setText("")
        self.lPref.setObjectName("lPref")
        self.lPlay = MyLabel(self.wButtonContainer)
        self.lPlay.setGeometry(QtCore.QRect(38, 0, 44, 32))
        self.lPlay.setMinimumSize(QtCore.QSize(44, 32))
        self.lPlay.setMaximumSize(QtCore.QSize(44, 32))
        self.lPlay.setStyleSheet("QLabel  {background:  url(\":/images/play_btn.png\")}\n"
"QLabel:hover {background:  url(\":/images/play_btn_pressed.png\") }")
        self.lPlay.setText("")
        self.lPlay.setObjectName("lPlay")
        self.lStop = MyLabel(self.wButtonContainer)
        self.lStop.setGeometry(QtCore.QRect(75, 0, 44, 32))
        self.lStop.setMinimumSize(QtCore.QSize(44, 32))
        self.lStop.setMaximumSize(QtCore.QSize(44, 32))
        self.lStop.setStyleSheet("QLabel  {background:  url(\":/images/stop_btn.png\") }\n"
"QLabel:hover {background:  url(\":/images/stop_btn_pressed.png\")}")
        self.lStop.setText("")
        self.lStop.setObjectName("lStop")
        self.lNext = MyLabel(self.wButtonContainer)
        self.lNext.setGeometry(QtCore.QRect(112, 0, 44, 32))
        self.lNext.setMinimumSize(QtCore.QSize(44, 32))
        self.lNext.setMaximumSize(QtCore.QSize(44, 32))
        self.lNext.setStyleSheet("QLabel  {background:  url(\":/images/next_btn.png\") }\n"
"QLabel:hover {background:  url(\":/images/next_btn_pressed.png\")}")
        self.lNext.setText("")
        self.lNext.setObjectName("lNext")
        self.horizontalLayout_3.addWidget(self.wButtonContainer)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.lLoop = MyLabel(self.btn_panel)
        self.lLoop.setMinimumSize(QtCore.QSize(32, 32))
        self.lLoop.setMaximumSize(QtCore.QSize(32, 32))
        self.lLoop.setStyleSheet("QLabel  {background:  url(\":/images/loop.png\") }\n"
"QLabel:hover {background:  url(\":/images/loop_h.png\")}")
        self.lLoop.setText("")
        self.lLoop.setObjectName("lLoop")
        self.horizontalLayout_3.addWidget(self.lLoop)
        self.lEq = MyLabel(self.btn_panel)
        self.lEq.setMinimumSize(QtCore.QSize(32, 32))
        self.lEq.setMaximumSize(QtCore.QSize(32, 32))
        self.lEq.setStyleSheet("QLabel  {background:  url(\":/images/eq.png\") }\n"
"QLabel:hover {background:  url(\":/images/eq_h.png\")}")
        self.lEq.setText("")
        self.lEq.setObjectName("lEq")
        self.horizontalLayout_3.addWidget(self.lEq)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_2.addWidget(self.btn_panel)
        self.w_volume = QtWidgets.QWidget(self.w_controls)
        self.w_volume.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_volume.sizePolicy().hasHeightForWidth())
        self.w_volume.setSizePolicy(sizePolicy)
        self.w_volume.setMinimumSize(QtCore.QSize(50, 0))
        self.w_volume.setStyleSheet("")
        self.w_volume.setObjectName("w_volume")
        self.horizontalLayout_2.addWidget(self.w_volume)
        self.verticalLayout_2.addWidget(self.w_controls)
        self.hl_plalistselect = QtWidgets.QHBoxLayout()
        self.hl_plalistselect.setSpacing(2)
        self.hl_plalistselect.setObjectName("hl_plalistselect")
        self.comboBox = MyComboBox(self.centralwidget)
        self.comboBox.setStyleSheet("QComboBox {\n"
"    background: rgba(0, 0, 0, 60);\n"
"    border-radius: 2px;\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-color: #445;\n"
"\n"
"};")
        self.comboBox.setObjectName("comboBox")
        self.hl_plalistselect.addWidget(self.comboBox)
        self.l_addplaylist = MyLabel(self.centralwidget)
        self.l_addplaylist.setMinimumSize(QtCore.QSize(24, 24))
        self.l_addplaylist.setMaximumSize(QtCore.QSize(24, 24))
        self.l_addplaylist.setStyleSheet("QLabel  {background:  url(\":/images/add.png\") }\n"
"QLabel:hover {background:  url(\":/images/add_h.png\")}")
        self.l_addplaylist.setText("")
        self.l_addplaylist.setObjectName("l_addplaylist")
        self.hl_plalistselect.addWidget(self.l_addplaylist)
        self.l_editplaylist = MyLabel(self.centralwidget)
        self.l_editplaylist.setMinimumSize(QtCore.QSize(24, 24))
        self.l_editplaylist.setMaximumSize(QtCore.QSize(24, 24))
        self.l_editplaylist.setStyleSheet("QLabel  {background:  url(\":/images/edit.png\") }\n"
"QLabel:hover {background:  url(\":/images/edit_h.png\")}")
        self.l_editplaylist.setText("")
        self.l_editplaylist.setObjectName("l_editplaylist")
        self.hl_plalistselect.addWidget(self.l_editplaylist)
        self.l_delplaylist = MyLabel(self.centralwidget)
        self.l_delplaylist.setMinimumSize(QtCore.QSize(24, 24))
        self.l_delplaylist.setMaximumSize(QtCore.QSize(24, 24))
        self.l_delplaylist.setStyleSheet("QLabel  {background:  url(\":/images/del.png\") }\n"
"QLabel:hover {background:  url(\":/images/del_h.png\")}")
        self.l_delplaylist.setText("")
        self.l_delplaylist.setObjectName("l_delplaylist")
        self.hl_plalistselect.addWidget(self.l_delplaylist)
        self.verticalLayout_2.addLayout(self.hl_plalistselect)
        self.listView = MyListView(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.listView.setFont(font)
        self.listView.setStyleSheet('''QListView {
    background: rgba(0, 0, 0, 60);
    border-style: inset;
    border-width: 1px;
    border-color: #445;
    color: #999;
    border-radius: 10px;}
QListView::item:selected { background: rgba(0, 0, 0, 60); border-width: 1px; border-style: inset; border-color: #345; border-radius: 6px; color: #fff;}
QListView::item:focus { background: rgba(0, 30, 60, 90); border-width: 1px; border-style: inset; border-color: #345; border-radius: 6px;}
QListView::item:focus:hover { background: rgba(0, 30, 60, 90); color: #fff;}
QListView::item:hover { background: transparent; color: #eee;}
QListView::item:selected:hover {background: rgba(0, 0, 0, 60); color:  aqua;}''')
        self.listView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.listView.setIconSize(QtCore.QSize(24, 24))
        self.listView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listView.setObjectName("listView")
        self.verticalLayout_2.addWidget(self.listView)
        self.hl_plalistselect_2 = QtWidgets.QHBoxLayout()
        self.hl_plalistselect_2.setSpacing(10)
        self.hl_plalistselect_2.setObjectName("hl_plalistselect_2")
        self.l_addfile = MyLabel(self.centralwidget)
        self.l_addfile.setMinimumSize(QtCore.QSize(24, 24))
        self.l_addfile.setMaximumSize(QtCore.QSize(24, 24))
        self.l_addfile.setStyleSheet("QLabel  {background:  url(\":/images/add.png\") }\n"
"QLabel:hover {background:  url(\":/images/add_h.png\")}")
        self.l_addfile.setText("")
        self.l_addfile.setObjectName("l_addfile")
        self.hl_plalistselect_2.addWidget(self.l_addfile)
        self.l_delfile = MyLabel(self.centralwidget)
        self.l_delfile.setMinimumSize(QtCore.QSize(24, 24))
        self.l_delfile.setMaximumSize(QtCore.QSize(24, 24))
        self.l_delfile.setStyleSheet("QLabel  {background:  url(\":/images/del.png\") }\n"
"QLabel:hover {background:  url(\":/images/del_h.png\")}")
        self.l_delfile.setText("")
        self.l_delfile.setObjectName("l_delfile")
        self.hl_plalistselect_2.addWidget(self.l_delfile)
        self.l_clearplaylist = MyLabel(self.centralwidget)
        self.l_clearplaylist.setMinimumSize(QtCore.QSize(24, 24))
        self.l_clearplaylist.setMaximumSize(QtCore.QSize(24, 24))
        self.l_clearplaylist.setStyleSheet("QLabel  {background:  url(\":/images/clear.png\") }\n"
"QLabel:hover {background:  url(\":/images/clear_h.png\")}")
        self.l_clearplaylist.setText("")
        self.l_clearplaylist.setObjectName("l_clearplaylist")
        self.hl_plalistselect_2.addWidget(self.l_clearplaylist)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hl_plalistselect_2.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.hl_plalistselect_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AudioPlayer"))
        self.l_time.setText(_translate("MainWindow", "0:00 / 0:00"))
        self.l_addplaylist.setToolTip(_translate("MainWindow", "Добавить плейлист"))
        self.l_editplaylist.setToolTip(_translate("MainWindow", "Переименовать плейлист"))
        self.l_delplaylist.setToolTip(_translate("MainWindow", "Удалить плейлист"))
        self.l_addfile.setToolTip(_translate("MainWindow", "Добавить файл в плейлист"))
        self.l_delfile.setToolTip(_translate("MainWindow", "Удалить файл из плейлиста"))
        self.l_clearplaylist.setToolTip(_translate("MainWindow", "Очистить плейлист"))
import images_rc
