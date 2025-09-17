import json
import os.path

from PySide6 import QtGui, QtCore,QtWidgets
from eqwindow import Ui_eq_window
from eqslider import EqSlider
from eqsettings import show_eq_settings
from lang import tr


def set_item_icon(icon_fn):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(icon_fn), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    return icon


class Equalizer(QtWidgets.QWidget):
    on_close = QtCore.Signal()

    def __init__(self, player=None, presets_filename=None):
        super(Equalizer, self).__init__()
        self.ui = Ui_eq_window()
        self.ui.setupUi(self)
        self.presets_filename = presets_filename
        self.player = player
        self.w_barsLayout = QtWidgets.QHBoxLayout(self.ui.w_bars)
        self.w_barsLayout.setContentsMargins(0, 2, 0, 2)
        self.w_barsLayout.setSpacing(0)
        self.w_barsLayout.setObjectName("w_barsLayout")
        self.ui.bClose.clicked.connect(self.close)
        self.ui.bMenu.clicked.connect(self.show_menu)
        self.sliderlist = []
        self.presets = []
        self.enable_presets = self.presets_filename is not None and len(self.presets_filename) > 0

        if self.enable_presets and os.path.isfile(self.presets_filename):
            try:
                with open(self.presets_filename, 'r') as f:
                    self.presets = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                self.presets = []

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
        reset_action = QtGui.QAction(tr('tool_tip_reset_eq'))
        reset_action.triggered.connect(self.reset_eq)
        reset_icon = QtGui.QIcon(':images/reset_eq.png')
        reset_action.setIcon(reset_icon)
        settings_action = QtGui.QAction(tr('tool_tip_settings_eq'))
        settings_action.triggered.connect(self.show_settings)
        icon = QtGui.QIcon(':/images/set.png')
        settings_action.setIcon(icon)
        menu = QtWidgets.QMenu(self)
        if self.enable_presets:
            p_menu = QtWidgets.QMenu(menu)
            p_menu.setTitle(tr('presets'))
            p_menu.setIcon(QtGui.QIcon(':/images/eq_icon.png'))
            save_as_preset = QtGui.QAction(tr('save_bands'))
            save_as_preset.triggered.connect(self.save_preset)
            save_as_preset.setIcon(QtGui.QIcon(':/images/add_icon.png'))
            p_menu.addAction(save_as_preset)
            delete_preset = QtGui.QAction(tr('delete_preset'))
            delete_preset.triggered.connect(self.delete_preset)
            delete_preset.setIcon(QtGui.QIcon(':/images/close.png'))
            p_menu.addAction(delete_preset)
            if len(self.presets) > 0:
                p_menu.addSection("")
                for eq in self.presets:
                    action = QtGui.QAction(eq['name'])
                    action.triggered.connect(lambda: self.preset_apply(eq['items']))
                    action.setIcon(QtGui.QIcon(':/images/eq_icon.png'))
                    p_menu.addAction(action)
            menu.addMenu(p_menu)
        menu.addSection("")
        menu.addAction(reset_action)
        menu.addSection("")
        menu.addAction(settings_action)
        menu.setMinimumWidth(200)
        pos = self.ui.bMenu.mapToGlobal(QtCore.QPoint(-170,30))
        menu.exec(pos)

    def save_preset(self):
        if not self.enable_presets: return
        name, res = QtWidgets.QInputDialog.getText(self, tr('save_eq_bands'), tr('enter_name'))
        for i in range(len(self.presets)):
            if name == self.presets[i]['name']:
                if QtWidgets.QMessageBox.question(self, tr('preset_name_exists'), tr('change_preset')) == QtWidgets.QMessageBox.StandardButton.Yes:
                    items = []
                    for j in range(len(self.sliderlist)):
                        items.append(self.sliderlist[j].pos - 15)
                    self.presets[i]['items'] = items
                    self.save_presets()
                return
        if res and len(name) > 1:
            items = []
            for i in range(len(self.sliderlist)):
                items.append(self.sliderlist[i].pos - 15)
            self.presets.append({'name': name, 'items': items})
            self.save_presets()

    def delete_preset(self):
        if not self.enable_presets: return
        names = [eq['name'] for eq in self.presets]
        item, result = QtWidgets.QInputDialog.getItem(self, tr('presets'), tr('select_preset'), names)
        if result:
            for i in range(len(self.presets)):
                if item == self.presets[i]['name']:
                    del self.presets[i]
                    self.save_presets()
                    break

    def save_presets(self):
        if not self.enable_presets: return
        with open(self.presets_filename, 'w', encoding='utf-8') as f:
            json.dump(self.presets, f, ensure_ascii=False, indent=4)

    def preset_apply(self, items):
        for i in range(len(items)):
            sl = self.sliderlist[i]
            sl.setPos(items[i]+15)
            sl.lab.setText(str(items[i]))
            self.player.set_eqgain(i, items[i])

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

