from PyQt5 import QtGui, QtCore,QtWidgets
from eqwindow import Ui_eq_window
from eqslider import EqSlider


class Equalizer(QtWidgets.QWidget):
    on_close = QtCore.pyqtSignal()
    def __init__(self, player = None):
        super(Equalizer, self).__init__()
        self.ui = Ui_eq_window()
        self.ui.setupUi(self)

        self.player = player
        self.w_barsLayout = QtWidgets.QHBoxLayout(self.ui.w_bars)
        self.w_barsLayout.setContentsMargins(0, 2, 0, 2)
        self.w_barsLayout.setSpacing(0)
        self.w_barsLayout.setObjectName("w_barsLayout")
        self.ui.l_close.onClick.connect(self.close)
        self.sliderlist = []

        self.ui.cbEnable.setChecked(self.player.EqualizerEnabled)

        freqs = self.player.get_eqfreq()
        for i in range(len(freqs)):
            if freqs[i] < 1000:
                fr = str(freqs[i])+'Hz'
            else:
                fr = str(round(freqs[i] / 1000))+'kHz'

            swidget = QtWidgets.QWidget(self.ui.w_bars)
            swidget.setObjectName(f"slider_widget{i}")
            swidget.setMaximumSize(QtCore.QSize(30,16777215))
            l = QtWidgets.QVBoxLayout(swidget)
            l.setObjectName(f"l_slider{i}")
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(0)

            ltitle = QtWidgets.QLabel(swidget)
            ltitle.setObjectName(f'ltitle{i}')
            ltitle.setAlignment(QtCore.Qt.AlignCenter)
            ltitle.setText(fr)

            font = QtGui.QFont()
            font.setPointSize(7)
            font.setBold(False)
            font.setItalic(False)
            ltitle.setFont(font)

            l.addWidget(ltitle)
            pos = self.player.EQBands[i].Gain
            sl = EqSlider(swidget,curpos=round(pos+15), maxpos = 30)
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

    def sliderPosChange(self, slider, pos):
        slider.lab.setText(str(pos-15))

    def sliderPosChanged(self, slider, pos):
        slider.lab.setText(str(pos-15))
        self.player.set_eqgain(slider.sid, pos-15)

    def cbEnableToggled(self):
        self.player.set_eqeffect(self.ui.cbEnable.isChecked())

    def do_move(self, x, y):
        self.move(x, y)

    def closeEvent(self, event):
        self.on_close.emit()
        super().closeEvent(event)

