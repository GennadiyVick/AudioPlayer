
from PyQt5 import QtCore, QtGui, QtWidgets
from mywidgets import MyLabel, MyComboBox, MyListView, CaptionWidget, VerSizeWidget
from viswidget import VisWidget
from lang import tr


def labelstyle(images):
    if len(images) == 1:
        return 'QLabel {background:  url("'+images[0]+'") no-repeat center center }'
    elif len(images) == 2:
        return 'QLabel {background:  url("'+images[0]+'") no-repeat center center } QLabel:hover {background:  url("'+images[1]+'") no-repeat center center}'
    else: return ''


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(350, 460)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint) # | QtCore.Qt.Tool
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        MainWindow.setWindowTitle("AudioPlayer")
        MainWindow.setContentsMargins(14, 14, 14, 14)
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setColor(QtGui.QColor(0, 0, 0, 255))
        effect.setOffset(0)
        effect.setBlurRadius(18)
        #MainWindow.setGraphicsEffect(effect)

        #create central widget and main vertical layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet('''QWidget {background: #222; color: #ccc;}
QWidget#centralwidget {background: qlineargradient( x1:0 y1:0, x2:0 y2:1, stop:0 #222222, stop:0.5 #242d32, stop:1 #222);
border-style: inset; border-width: 1px; border-color: #191919; border-radius: 10px;}
QScrollBar {background: transparent; border-style: inset;border-radius: 5px;border-width: 0px;}
QScrollBar:vertical {width: 10px;}
QScrollBar::handle {margin: -1px; background: #444; border-style: inset;border-radius: 5px; border: 1px solid #1c1c1c;}
QScrollBar::handle:vertical {min-height: 10px;}
QScrollBar::handle:horizontal {min-width: 10px;}
QScrollBar::handle:hover {background: #555;}
QScrollBar::left-arrow, QScrollBar::right-arrow, QScrollBar::up-arrow,
QScrollBar::down-arrow, QScrollBar::sub-line, QScrollBar::add-line,
QScrollBar::add-page, QScrollBar::sub-page {background: transparent; height: 0; width: 0;}''')
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setGraphicsEffect(effect)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(7, 3, 7, 0)

        #caption layout
        self.hl_top = QtWidgets.QHBoxLayout()
        self.hl_top.setContentsMargins(0, 0, 0, 3)
        self.hl_top.setSpacing(6)
        self.hl_top.setObjectName("hl_top")
        self.title_icon = QtWidgets.QLabel(self.centralwidget)
        self.title_icon.setText('')
        self.title_icon.setMinimumSize(QtCore.QSize(24, 24))
        self.title_icon.setMaximumSize(QtCore.QSize(24, 24))
        self.title_icon.setPixmap(QtGui.QPixmap(':/images/headphones.png'))
        self.hl_top.addWidget(self.title_icon)
        self.caption_widget = CaptionWidget(MainWindow, self.centralwidget)
        self.caption_widget.caption = '- - AudioPlayer - -'
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.caption_widget.setFont(font)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.caption_widget.sizePolicy().hasHeightForWidth())
        self.hl_top.addWidget(self.caption_widget)

        self.lmin = MyLabel({'default': labelstyle([":/images/minimize.png", ":/images/minimize_h.png"])}, self.centralwidget)
        self.lmin.setMinimumSize(QtCore.QSize(18, 18))
        self.lmin.setMaximumSize(QtCore.QSize(18, 18))
        self.lmin.setText("")
        self.lmin.setObjectName("lmin")
        self.hl_top.addWidget(self.lmin)

        self.lclose = MyLabel({'default': labelstyle([":/images/close.png", ":/images/close_h.png"])}, self.centralwidget)
        self.lclose.setMinimumSize(QtCore.QSize(18, 18))
        self.lclose.setMaximumSize(QtCore.QSize(18, 18))
        self.lclose.setText("")
        self.lclose.setObjectName("lclose")
        self.hl_top.addWidget(self.lclose)
        self.verticalLayout_2.addLayout(self.hl_top)

        #info layout
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
        self.w_info.setStyleSheet("QWidget {background: transparent;}\n"
"QWidget#w_info {background: rgba(0, 0, 0, 60); border-style: inset;\n"
"border-width: 1px; border-color: #353838; border-radius: 10px;}")
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
        self.state_icon.setStyleSheet("background: transparent; border-width: 0px; border-radius: 0px;")
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
        self.l_time.setText("0:00 / 0:00")
        self.verticalLayout.addWidget(self.l_time)
        self.verticalLayout_2.addWidget(self.w_info)

        #track bar
        self.w_track = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_track.sizePolicy().hasHeightForWidth())
        self.w_track.setSizePolicy(sizePolicy)
        self.w_track.setMinimumSize(QtCore.QSize(0, 16))
        self.w_track.setStyleSheet("QWidget#w_track {\n"
"    background: rgba(0, 0, 0, 60); border-style: inset;\n"
"    border-width: 1px; border-color: #353535; border-radius: 7px};")
        self.w_track.setObjectName("w_track")
        self.verticalLayout_2.addWidget(self.w_track)

        #controls
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
        self.wButtonContainer.setMinimumSize(QtCore.QSize(190, 45))
        self.wButtonContainer.setMaximumSize(QtCore.QSize(190, 45))
        self.wButtonContainer.setObjectName("wButtonContainer")
        self.wButtonContainer.setStyleSheet("QWidget#wButtonContainer {\n"
"    background: #131013; border-style: inset; border-width: 1px;\n"
"    border-color: #60404050; border-radius: 10px;}")

        self.lPrev = MyLabel({'default':labelstyle([':/images/prev.png', ':/images/prev_over.png']), 'pressed':labelstyle([':/images/prev_down.png'])}, self.wButtonContainer)
        self.lPrev.setGeometry(QtCore.QRect(0, 0, 60, 45))
        self.lPrev.setText("")
        self.lPrev.setObjectName("lPrev")
        self.lPlay = MyLabel({'default':labelstyle([':/images/play.png', ':/images/play_over.png']), 'pressed':labelstyle([':/images/play_down.png'])}, self.wButtonContainer)
        self.lPlay.setGeometry(QtCore.QRect(43, 0, 60, 45))
        self.lPlay.setText("")
        self.lPlay.setObjectName("lPlay")
        self.lStop = MyLabel({'default':labelstyle([':/images/stop.png', ':/images/stop_over.png']), 'pressed':labelstyle([':/images/stop_down.png'])}, self.wButtonContainer)
        self.lStop.setGeometry(QtCore.QRect(86, 0, 60, 45))
        self.lStop.setText("")
        self.lStop.setObjectName("lStop")
        self.lNext = MyLabel({'default':labelstyle([':/images/next.png', ':/images/next_over.png']), 'pressed':labelstyle([':/images/next_down.png'])}, self.wButtonContainer)
        self.lNext.setGeometry(QtCore.QRect(129, 0, 60, 45))
        self.lNext.setText("")
        self.lNext.setObjectName("lNext")
        self.horizontalLayout_3.addWidget(self.wButtonContainer)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.lLoop = MyLabel({'default':labelstyle([':/images/loop_off.png',':/images/loop_off_over.png'])}, self.btn_panel)
        self.lLoop.setMinimumSize(QtCore.QSize(32, 32))
        self.lLoop.setMaximumSize(QtCore.QSize(32, 32))
        self.lLoop.setText("")
        self.lLoop.setObjectName("lLoop")
        self.horizontalLayout_3.addWidget(self.lLoop)
        self.lEq = MyLabel({'default': labelstyle([':/images/eq.png', ':/images/eq_h.png']),
                            'checked': labelstyle([':/images/eq_en.png', ':/images/eq_en_h.png'])}, self.btn_panel)
        self.lEq.setMinimumSize(QtCore.QSize(32, 32))
        self.lEq.setMaximumSize(QtCore.QSize(32, 32))
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

        #visualization widget
        self.viswidget = VisWidget(self.centralwidget)
        self.viswidget.setObjectName('viswidget')
        self.viswidget.setMinimumSize(QtCore.QSize(100, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viswidget.sizePolicy().hasHeightForWidth())
        self.viswidget.setSizePolicy(sizePolicy)
        self.verticalLayout_2.addWidget(self.viswidget)

        #playlist
        self.hl_plalistselect = QtWidgets.QHBoxLayout()
        self.hl_plalistselect.setSpacing(2)
        self.hl_plalistselect.setObjectName("hl_plalistselect")
        self.comboBox = MyComboBox(self.centralwidget)
        self.comboBox.setStyleSheet("QComboBox {\n"
"    background: rgba(0, 0, 0, 60);\n"
"    border-radius: 6px;\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-color: #334;\n"
"\n"
"};")
        self.comboBox.setObjectName("comboBox")
        self.hl_plalistselect.addWidget(self.comboBox)
        self.l_addplaylist = MyLabel({'default':labelstyle([':/images/add.png',':/images/add_h.png'])}, self.centralwidget)
        self.l_addplaylist.setMinimumSize(QtCore.QSize(24, 24))
        self.l_addplaylist.setMaximumSize(QtCore.QSize(24, 24))
        self.l_addplaylist.setText("")
        self.l_addplaylist.setObjectName("l_addplaylist")
        self.hl_plalistselect.addWidget(self.l_addplaylist)
        self.l_editplaylist =  MyLabel({'default':labelstyle([':/images/edit.png',':/images/edit_h.png'])}, self.centralwidget)
        self.l_editplaylist.setMinimumSize(QtCore.QSize(24, 24))
        self.l_editplaylist.setMaximumSize(QtCore.QSize(24, 24))
        self.l_editplaylist.setText("")
        self.l_editplaylist.setObjectName("l_editplaylist")
        self.hl_plalistselect.addWidget(self.l_editplaylist)
        self.l_delplaylist =  MyLabel({'default':labelstyle([':/images/del.png',':/images/del_h.png'])}, self.centralwidget)
        self.l_delplaylist.setMinimumSize(QtCore.QSize(24, 24))
        self.l_delplaylist.setMaximumSize(QtCore.QSize(24, 24))
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
        self.l_addfile =  MyLabel({'default':labelstyle([':/images/add.png',':/images/add_h.png'])}, self.centralwidget)
        self.l_addfile.setMinimumSize(QtCore.QSize(24, 24))
        self.l_addfile.setMaximumSize(QtCore.QSize(24, 24))
        self.l_addfile.setText("")
        self.l_addfile.setObjectName("l_addfile")
        self.hl_plalistselect_2.addWidget(self.l_addfile)
        self.l_delfile = MyLabel({'default':labelstyle([':/images/del.png',':/images/del_h.png'])}, self.centralwidget)
        self.l_delfile.setMinimumSize(QtCore.QSize(24, 24))
        self.l_delfile.setMaximumSize(QtCore.QSize(24, 24))
        self.l_delfile.setText("")
        self.l_delfile.setObjectName("l_delfile")
        self.hl_plalistselect_2.addWidget(self.l_delfile)
        self.l_clearplaylist = MyLabel({'default':labelstyle([':/images/clear.png',':/images/clear_h.png'])}, self.centralwidget)
        self.l_clearplaylist.setMinimumSize(QtCore.QSize(24, 24))
        self.l_clearplaylist.setMaximumSize(QtCore.QSize(24, 24))
        self.l_clearplaylist.setText("")
        self.l_clearplaylist.setObjectName("l_clearplaylist")
        self.hl_plalistselect_2.addWidget(self.l_clearplaylist)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hl_plalistselect_2.addItem(spacerItem2)
        self.l_version = QtWidgets.QLabel(self.centralwidget)
        self.l_version.setObjectName('l_version')
        self.l_version.setStyleSheet('QLabel#l_version{font-size: 7pt; color: #888;}')
        self.l_version.setText('v. 2.3')
        self.l_version.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight)
        self.hl_plalistselect_2.addWidget(self.l_version)
        self.verticalLayout_2.addLayout(self.hl_plalistselect_2)

        #bottom widget for vertical size change
        self.bottom_widget = VerSizeWidget(self.centralwidget)
        self.bottom_widget.setMinimumSize(QtCore.QSize(0, 4))
        self.bottom_widget.setMaximumSize(QtCore.QSize(2048, 4))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.bottom_widget.setSizePolicy(sizePolicy)
        self.bottom_widget.setStyleSheet('background: transparent;')
        self.bottom_widget.setObjectName('bottom_widget')
        self.bottom_widget.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.verticalLayout_2.addWidget(self.bottom_widget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.l_addplaylist.setToolTip(tr("add_playlist"))
        self.l_editplaylist.setToolTip(tr("rename_playlist"))
        self.l_delplaylist.setToolTip(tr("remove_playlist"))
        self.l_addfile.setToolTip(tr("add_track_to_playlist"))
        self.l_delfile.setToolTip(tr("remove_track"))
        self.l_clearplaylist.setToolTip(tr("clear_playlist"))
import images_rc
