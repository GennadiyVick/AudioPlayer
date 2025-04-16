from PyQt5 import QtGui, QtCore,QtWidgets
from eqwindow import Ui_eq_window
from eqslider import EqSlider
from eqsettings import show_eq_settings
from lang import tr


def set_item_icon(icon_fn):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(icon_fn), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    return icon

class Equalizer(QtWidgets.QWidget):
    on_close = QtCore.pyqtSignal()

    def __init__(self, player=None):
        super(Equalizer, self).__init__()
        self.ui = Ui_eq_window()
        self.ui.setupUi(self)

        self.player = player
        self.w_barsLayout = QtWidgets.QHBoxLayout(self.ui.w_bars)
        self.w_barsLayout.setContentsMargins(0, 2, 0, 2)
        self.w_barsLayout.setSpacing(0)
        self.w_barsLayout.setObjectName("w_barsLayout")
        self.ui.bClose.clicked.connect(self.close)
        #self.ui.bSettings.onClick.connect(self.show_settings)
        #self.ui.l_reset.onClick.connect(self.reset_eq)
        self.ui.bMenu.clicked.connect(self.show_menu)
        self.sliderlist = []

        self.ui.cbEnable.setChecked(self.player.EqualizerEnabled)
        self.band_title_l = []
        freqs = self.player.get_eqfreq()
        for i in range(len(freqs)):
            if freqs[i] < 1000:
                fr = str(freqs[i])+'Hz'
            else:
                fr = round(freqs[i] / 1000, 1)
                fr2 = freqs[i] // 1000
                if fr == fr2:
                   fr = fr2
                fr = str(fr)+'kHz'

            swidget = QtWidgets.QWidget(self.ui.w_bars)
            swidget.setObjectName(f"slider_widget{i}")
            swidget.setMaximumSize(QtCore.QSize(30, 16777215))
            l = QtWidgets.QVBoxLayout(swidget)
            l.setObjectName(f"l_slider{i}")
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(0)

            ltitle = QtWidgets.QLabel(swidget)
            ltitle.setObjectName(f'ltitle{i}')
            ltitle.setAlignment(QtCore.Qt.AlignCenter)
            ltitle.setText(fr)
            self.band_title_l.append(ltitle)

            font = QtGui.QFont()
            font.setPointSize(7)
            font.setBold(False)
            font.setItalic(False)
            ltitle.setFont(font)

            l.addWidget(ltitle)
            pos = self.player.EQBands[i].Gain
            sl = EqSlider(swidget, curpos=round(pos+15), maxpos=30)
            sl.setObjectName(f'eqs{i}')
            sl.sid = i
            sl.posChanged.connect(self.sliderPosChanged)
            sl.posChange.connect(self.sliderPosChange)
            self.sliderlist.append(sl)
            l.addWidget(sl)

            lab = QtWidgets.QLabel(swidget)
            lab.setObjectName(f'slabel{i}')
            lab.setAlignment(QtCore.Qt.AlignCenter)
            lab.setFont(font)
            lab.setText(str(int(pos)))
            l.addWidget(lab)
            sl.lab = lab
            sl.ltitle = ltitle
            self.w_barsLayout.addWidget(swidget)

        self.ui.cbEnable.toggled.connect(self.cbEnableToggled)


    def show_menu(self):
        #menu = QtWidgets.QMenu(self)
        #settings_action = QtWidgets.QAction(tr("tool_tip_settings_eq"))
        #settings_action.setIcon(set_item_icon(":/images/set.png"))
        #settings_action.triggered.connect(self.show_settings)
        #menu.exec_(QtCore.QPoint(0, 0))
        reset_action = QtWidgets.QAction(tr('tool_tip_reset_eq'))
        reset_action.triggered.connect(self.reset_eq)
        reset_icon = QtGui.QIcon(':images/reset_eq.png')
        reset_action.setIcon(reset_icon)
        settings_action = QtWidgets.QAction(tr('tool_tip_settings_eq'))
        settings_action.triggered.connect(self.show_settings)
        icon = QtGui.QIcon(':/images/set.png')
        settings_action.setIcon(icon)
        menu = QtWidgets.QMenu(self)
        menu.addAction(reset_action)
        menu.addSection("")
        menu.addAction(settings_action)
        menu.setMinimumWidth(200)
        pos = self.ui.bMenu.mapToGlobal(QtCore.QPoint(-170,30))
        menu.exec_(pos)

    def sliderPosChange(self, slider, pos):
        slider.lab.setText(str(pos-15))

    def sliderPosChanged(self, slider, pos):
        slider.lab.setText(str(pos-15))
        self.player.set_eqgain(slider.sid, pos-15)

    def reset_eq(self):
        for sl in self.sliderlist:
            sl.setPos(15)
            sl.lab.setText('0')
            self.player.set_eqgain(sl.sid, 0)

    def cbEnableToggled(self):
        self.player.set_eqeffect(self.ui.cbEnable.isChecked())

    def do_move(self, x, y):
        self.move(x, y)

    def closeEvent(self, event):
        self.on_close.emit()
        super().closeEvent(event)

    def update_bands_title(self):
        for i, b in enumerate(self.player.EQBands):
            if b.CenterFreq < 1000:
                fr = str(b.CenterFreq)+'Hz'
            else:
                fr = round(b.CenterFreq / 1000, 1)
                fr2 = b.CenterFreq // 1000
                if fr == fr2:
                    fr = fr2
                fr = str(fr)+'kHz'
            self.band_title_l[i].setText(fr)

    def show_settings(self):
        freq_l = [b.CenterFreq for b in self.player.EQBands]
        bw_l = [b.Bandwidth for b in self.player.EQBands]
        bands = show_eq_settings(self, freq_l, bw_l)
        if len(bands) > 0:
            self.player.update_eq_bands(bands)
            self.update_bands_title()

