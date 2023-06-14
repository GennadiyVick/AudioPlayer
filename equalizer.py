import sys
import os
from PyQt5 import QtGui, QtCore,QtWidgets
from eqwindow import Ui_eq_window
from eqslider import EqSlider
import vlc
import images_rc



class Equalizer(QtWidgets.QWidget):
    def __init__(self, player = None, parent=None):
        super(Equalizer, self).__init__()
        self.qApp = parent
        self.ui = Ui_eq_window()
        self.ui.setupUi(self)
        self.player = player
        self.w_barsLayout = QtWidgets.QHBoxLayout(self.ui.w_bars)
        self.w_barsLayout.setContentsMargins(0, 2, 0, 2)
        self.w_barsLayout.setSpacing(0)
        self.w_barsLayout.setObjectName("w_barsLayout")
        self.ui.label_2.onMousePress.connect(self.titleMousePress)
        self.ui.label_2.onMouseMove.connect(self.titleMouseMove)
        self.ui.l_addplaylist_2.onClick.connect(self.close)
        #self.ui.label_2.onMouseRelease.connect(self.titleMouseRelease)
        self.mx = 0
        self.my = 0
        self.sliderlist = []
        self.ps = self.pos()
        self.set = QtCore.QSettings(os.path.join('RoganovSoft', 'AudioPlayer'), "config")
        self.isCustom = self.player.presetname == "custom"
        self.ui.cbPreset.addItem('')
        for presetname in self.player.presets:
            self.ui.cbPreset.addItem(presetname)

        self.ui.cbEnable.setChecked(self.player.equalizerenabled)
        self.preset = [20 for i in range(self.player.bandcount)]

        if self.isCustom:
            self.ui.cbPreset.setCurrentIndex(0)
            self.preset = self.player.custompreset.copy()
        else:
            self.preset = [20 for i in range(self.player.bandcount)]
            self.preset[0] = round(self.player.equalizer.get_preamp()+20)
            for i in range(1, self.player.bandcount):
                self.preset[i] = round(self.player.equalizer.get_amp_at_index(i-1)+20)
        freqs = ['Pre_amp']
        for i in range(1, self.player.bandcount):
            fr = vlc.libvlc_audio_equalizer_get_band_frequency(i-1)
            if fr < 1000:
                freqs.append(str(round(fr))+'Hz')
            else:
                freqs.append(str(round(fr / 1000))+'kHz')


        for i in range(self.player.bandcount):
            #

            swidget = QtWidgets.QWidget(self.ui.w_bars)
            swidget.setObjectName(f"slider_widget{i}")
            #swidget.setStyleSheet('QWidget#slider_widget'+str(i)+'{ background: #111;}')
            swidget.setMaximumSize(QtCore.QSize(30,16777215))
            l = QtWidgets.QVBoxLayout(swidget)
            l.setObjectName(f"l_slider{i}")
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(0)

            ltitle = QtWidgets.QLabel(swidget)
            ltitle.setObjectName(f'ltitle{i}')
            ltitle.setAlignment(QtCore.Qt.AlignCenter)
            ltitle.setText(freqs[i])

            font = QtGui.QFont()
            font.setPointSize(7)
            font.setBold(False)
            font.setItalic(False)
            ltitle.setFont(font)

            l.addWidget(ltitle)

            sl = EqSlider(swidget,self.preset[i], 40)
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
            lab.setText(str(self.preset[i] - sl.maxpos // 2))
            l.addWidget(lab)
            sl.lab = lab
            sl.ltitle = ltitle
            self.w_barsLayout.addWidget(swidget)
        self.presetToGui()
        self.ui.cbEnable.toggled.connect(self.cbEnableToggled)
        self.ui.cbPreset.activated.connect(self.cbPresetActivated)
        #self.ui.l_addpreset.onClick.connect(self.addPresetClick)

    def sliderPosChanged(self, slider, pos):
        self.sliderPosChange(slider,pos)
        if not self.isCustom:
            self.isCustom = True
            self.player.presetname = "custom"
            self.ui.cbPreset.setCurrentIndex(0)
            self.player.custompreset = self.preset.copy()
        else:
            self.player.custompreset[slider.sid] = pos
        if slider.sid > 0:
            self.player.equalizer.set_amp_at_index(pos-20, slider.sid-1)
        else:
            r = self.player.equalizer.set_preamp(pos-20)

        presetname = self.set.value("EQ_preset","custom")
        if presetname != self.player.presetname:
            self.set.setValue("EQ_preset",self.player.presetname)
            for i in range(self.player.bandcount):
                self.set.setValue(f"EQ_customPreset_{i}", self.preset[i])
        else:
            self.set.setValue(f"EQ_customPreset_{slider.sid}", self.preset[slider.sid])
        if self.ui.cbEnable.isChecked():
            self.player.mediaplayer.set_equalizer(self.player.equalizer)
        #self.custompreset = [set.value(f"EQ_customPreset_{i}", 20) for i in range(self.bcount)]

    def sliderPosChange(self, slider, pos):
        slider.lab.setText(str(pos - 20))
        self.preset[slider.sid] = pos


    def cbEnableToggled(self):
        if self.ui.cbEnable.isChecked():
            self.player.mediaplayer.set_equalizer(self.player.equalizer)
        else:
            self.player.mediaplayer.set_equalizer(None)
        self.set.setValue("EQ_enabled",'True' if self.ui.cbEnable.isChecked() else 'False')
        self.preset[0] = round(self.player.equalizer.get_preamp()+20)
        for i in range(1, self.player.bandcount):
            self.preset[i] = round(self.player.equalizer.get_amp_at_index(i-1)+20)

    def cbPresetActivated(self, index):
        if index < 1:
            self.player.presetname = "custom"
            self.set.setValue("EQ_preset",self.player.presetname)
            self.presets = self.player.custompreset.copy()
            self.player.equalizer.set_preamp(self.preset[0]-20)
            for i in range(1, self.player.bandcount):
                self.player.equalizer.set_amp_at_index(self.preset[i]-20,i-1)
            self.presetToGui()
            self.isCustom = True
            return

        presetname = self.ui.cbPreset.itemText(index)
        if presetname in self.player.presets:
            self.isCustom = False
            i = self.player.presets.index(presetname)
            self.player.presetname = presetname
            self.set.setValue("EQ_preset",self.player.presetname)
            vlc.libvlc_audio_equalizer_release(self.player.equalizer)
            self.player.equalizer = vlc.libvlc_audio_equalizer_new_from_preset(i)
            if self.player.equalizerenabled:
                self.player.mediaplayer.set_equalizer(self.player.equalizer)
            self.preset[0] = round(self.player.equalizer.get_preamp()+20)
            for i in range(1, self.player.bandcount):
                self.preset[i] = round(self.player.equalizer.get_amp_at_index(i-1)+20)

            self.presetToGui()

    def presetToGui(self):
        for i in range(self.player.bandcount):
            self.sliderlist[i].setPos(self.preset[i])
            self.sliderlist[i].lab.setText(str(self.preset[i] - 20))
    
    def titleMousePress(self, event):
        self.my = event.globalPos().y()
        self.mx = event.globalPos().x()
        self.ps = self.pos()

    def titleMouseMove(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            y = self.ps.y()+(event.globalPos().y()-self.my)
            x = self.ps.x()+(event.globalPos().x()-self.mx)
            self.move(x,y)

    def closeEvent(self, event):
        '''
        set = QtCore.QSettings(os.path.join('RoganovSoft', 'AudioPlayer'), "config")
        set.setValue(f"EQ_preset",self.presetname)
        #self.custompreset = [set.value(f"EQ_customPreset_{i}", 20) for i in range(self.bcount)]
        if self.isCustom:
            self.custompreset = self.preset.copy()
        for i in range(len(self.custompreset)):
            set.setValue(f"EQ_customPreset_{i}", self.custompreset[i])
        '''
        if __name__ == '__main__':
            self.qApp.quit()
        else:
            super(Equalizer,self).closeEvent(event)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Equalizer(None, app)
    app.mainwindow = main
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
