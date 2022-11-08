#!/usr/bin/python3
'''
Audio player using libvlc and pyqt5

INSTALLATION
Window:
    1. download and install python from https://www.python.org/downloads/windows/
    in console...
    2. python -m pip install PyQt5
    3. python -m pip install python-vlc
Linux:
    Most Linux distributions have Python3 pre-installed.
    1. sudo apt-get install python3-pip
    2. pip3 install PyQt5
    3. pip3 install python3-vlc

Authon Roganov G.V. roganovg@mail.ru
'''

import sys
import os
from PyQt5 import QtGui, QtCore,QtWidgets
from mainwindow import Ui_MainWindow
from mvolume import MVolume
from player import Player
from mslider import MSlider
from equalizer import Equalizer

class AudioPlayer(QtWidgets.QMainWindow):
    #Создание окна
    def __init__(self, parent=None):
        super(AudioPlayer, self).__init__(None)
        #создание основных контролов и лейаутов происходит в классе Ui_MainWindow модуля mainwindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #path - путь к плейлистам, указан путь к данному скрипту,
        #однако правильней было бы его перенести в каталог пользователя.
        self.path = os.path.dirname(os.path.realpath(__file__))
        #cоздаю свой контрол управления громкостью
        self.createVolumeControl()
        #контрол управления временем/позицией
        self.createSlider()
        #класс Player управляет воспроизведением и вызовами к libvlc
        self.player = Player()
        self.model = QtGui.QStandardItemModel(self)
        self.ui.listView.setModel(self.model)
        #разрешаем перетаскивание на форму
        self.setAcceptDrops(True)

        #связываем сингалы/события с слотами/процедурами
        self.setEvent()
        #добавляю пустой элемент, это временный плейлист
        self.ui.comboBox.addItem('')

        #грузим плейлисты
        files = os.listdir(self.path)
        for fn in files:
            if fn != 'default.plt' and fn[-4:].lower() == '.plt':
                self.ui.comboBox.addItem(fn[:-4])
        #проверяем входящие аргументы,если аудио файл открыли с помощью этого скрипта
        self.checkargv()
        #грузим настройки
        self.loadSets()

        self.eqdialog = None

    #связываем события со слотами
    def setEvent(self):
        self.player.stateChanged.connect(self.onPlayerStateChanged)
        self.player.volumeChanged.connect(self.vol.setPos)
        self.player.positionChanged.connect(self.playerPosChanged)
        self.player.playlistIndexChanged.connect(self.onPlayerPlaylistIndexChanged)
        self.player.playingFileChanged.connect(self.onPlayerFileChanged)

        self.vol.posChanged.connect(self.player.set_volume)
        self.slider.posChanged.connect(self.onSliderPosChanged)

        self.ui.listView.doubleClicked.connect(self.listviewdoubleClicked)
        self.ui.lPlay.onClick.connect(self.player.play_pause)
        self.ui.lStop.onClick.connect(self.player.stop)
        self.ui.lPref.onClick.connect(self.player.prev)
        self.ui.lNext.onClick.connect(self.player.next)
        self.ui.lLoop.onClick.connect(self.setLoop)
        self.ui.l_delfile.onClick.connect(self.delFromPlayList)
        self.ui.l_clearplaylist.onClick.connect(self.clearPlayList)
        self.ui.l_addfile.onClick.connect(self.addFilePlayList)
        self.ui.l_addplaylist.onClick.connect(self.addPlayList)
        self.ui.l_delplaylist.onClick.connect(self.delPlayList)
        self.ui.l_editplaylist.onClick.connect(self.editPlayList)
        self.ui.lEq.onClick.connect(self.eqClick)
        self.ui.comboBox.activated.connect(self.comboBoxActivated)

        #регистрируем класс QAction исключительно для shortcut -  пробел для вызова паузы или плей
        # но вероятнее всего это не работает. т.к. фокус перехватывается контролами ComboBox(список плейлистов) и listView(плейлист)
        #в связи с этим я переопределил эти компоненты см. модуль mywidgets классы MyComboBox и MyListView
        self.ui.comboBox.keyPressed.connect(self.controlKeyPressed)
        self.ui.listView.keyPressed.connect(self.controlKeyPressed)

        self.actionPlayPause = QtWidgets.QAction(self)
        self.actionPlayPause.setObjectName("actionPlayPause")
        self.actionPlayPause.setShortcut("Space")
        self.actionPlayPause.triggered.connect(self.player.play_pause)


    #private slots...
    #ОБРАТНЫЕ вызовы от плеера .....

    def onPlayerStateChanged(self, state):
        if state == Player.STATE_STOP:
            self.ui.state_icon.setPixmap(QtGui.QPixmap(':/images/stop_state.png'))
            self.slider.posChange(0)
            self.timeChange()
            self.duration = 0
        elif state == Player.STATE_PLAY:
            self.ui.state_icon.setPixmap(QtGui.QPixmap(':/images/play_state.png'))
        elif state == Player.STATE_PAUSE:
            self.ui.state_icon.setPixmap(QtGui.QPixmap(':/images/pause_state.png'))

        if state == Player.STATE_STOP or state == Player.STATE_PAUSE:
            self.ui.lPlay.setStyleSheet("QLabel  {background:  url(\":/images/play_btn.png\")}\n"
"QLabel:hover {background:  url(\":/images/play_btn_pressed.png\") }")
        else:
            self.ui.lPlay.setStyleSheet("QLabel  {background:  url(\":/images/pause_btn.png\")}\n"
"QLabel:hover {background:  url(\":/images/pause_btn_pressed.png\") }")


    def onPlayerPlaylistIndexChanged(self, index):
        self.ui.listView.clearSelection()
        self.ui.listView.selectionModel().select(self.model.index(index,0), QtCore.QItemSelectionModel.Toggle)


    def onPlayerFileChanged(self):
        info = self.player.getCurrentInfo()
        self.duration = self.player.getLength()
        self.ui.l_info.setText(os.path.basename(info['filename']))

    def playerPosChanged(self, pos):
        self.slider.posChange(pos)
        self.timeChange()

    #Прочие методы событий.......


    def onSliderPosChanged(self, pos):
        self.player.set_position(pos)
        self.timeChange()

    def timeChange(self):
        self.ui.l_time.setText(self.player.getTimePos()+' / '+self.player.getTimeDuration())

    def listviewdoubleClicked(self, index):
        self.player.playByIndex(index.row())

    def delFromPlayList(self):
        if len(self.player.playlist) == 0: return
        i =  self.ui.listView.currentIndex().row()
        if i < 0: return
        self.player.playlist.pop(i)
        self.model.removeRow(i)
        self.savePlayList()

    def clearPlayList(self):
        if len(self.player.playlist) == 0: return
        self.player.playlist.clear()
        self.model.clear()
        self.savePlayList()

    def addFilePlayList(self):
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Выбор файла...", filter='MUSIC (*.mp3 *.wma, *.m4a, *.wav)')
        if not filenames: return
        self.player.addFiles(filenames)
        for fn in filenames:
            self.model.appendRow(QtGui.QStandardItem(QtGui.QIcon(":/images/playlist_icon.png"), os.path.basename(fn)))

    def addPlayList(self):
        #text = QtWidgets.QInputDialog.getText(self, "Добавить плейлист","Введите имя плейлиста", QtWidgets.QLineEdit.Normal,'~', ok)
        text, ok = QtWidgets.QInputDialog.getText(self, "Добавить плейлист","Введите имя плейлиста", QtWidgets.QLineEdit.Normal)
        if ok and len(text) > 0:
            self.ui.comboBox.addItem(text)
            self.ui.comboBox.setCurrentIndex(self.ui.comboBox.count()-1)
            self.savePlayList()
            fn = os.path.join(self.path,'default.plt')
            if os.path.isfile(fn): os.remove(fn)

    def comboBoxActivated(self, index):
        self.loadPlayList()

    def delPlayList(self):
        i = self.ui.comboBox.currentIndex()
        if i < 1: return
        #r = QtWidgets.QMessageBox.Question()
        r = QtWidgets.QMessageBox.question(None,'Внимание!!!',"Удалить текущий плейлист?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if r != QtWidgets.QMessageBox.Yes: return
        fn = os.path.join(self.path,self.ui.comboBox.itemText(i)+'.plt')
        if os.path.isfile(fn): os.remove(fn)
        self.ui.comboBox.removeItem(i)
        if i < self.ui.comboBox.count():
            self.ui.comboBox.setCurrentIndex(i)
        else:
            self.ui.comboBox.setCurrentIndex(self.ui.comboBox.count()-1)
        self.loadPlayList()

    def editPlayList(self):
        i = self.ui.comboBox.currentIndex()
        if i < 1: return
        ptext = self.ui.comboBox.itemText(i)
        text, ok = QtWidgets.QInputDialog.getText(self, "Переименовать плейлист","Введите новое имя плейлиста", QtWidgets.QLineEdit.Normal, ptext)
        if not ok or len(text) < 1 or text == ptext:
            return
        fn = os.path.join(self.path,ptext+'.plt')
        if os.path.isfile(fn): os.remove(fn)
        self.ui.comboBox.setItemText(i, text)
        self.savePlayList()


    def eqClick(self):
        if self.eqdialog == None:
            self.eqdialog = Equalizer(self.player, self)
        rect = QtWidgets.QApplication.desktop().screen().rect()

        if self.pos().x() < rect.width() // 2:
            x = self.pos().x()+self.width()+4
        else:
            x = self.pos().x() - self.eqdialog.width() - 4

        self.eqdialog.move(x, self.pos().y())
        self.eqdialog.show()


    #это обратный вызов от Combobox и ListView
    def controlKeyPressed(self, event):
        if event.key() == 32:
            self.player.play_pause()
        elif event.key() == 16777220: #ENTER от ListView
            if len(self.player.playlist) == 0: return
            i =  self.ui.listView.currentIndex().row()
            if i < 0: return
            for index in self.ui.listView.selectedIndexes():
                if i == index.row(): return
            self.player.playByIndex(i)



    def setLoop(self, default = None):
        if default != None:
            loop = default
        else:
            loop = self.player.loop
            if loop == Player.LOOP_TOEND:
                loop = Player.LOOP_REPEAT
            else:
                loop = Player.LOOP_TOEND
        self.player.loop = loop
        if loop == Player.LOOP_TOEND:
            self.ui.lLoop.setStyleSheet("QLabel  {background:  url(\":/images/loop.png\") }\n"
"QLabel:hover {background:  url(\":/images/loop_h.png\")}")
        else:
            self.ui.lLoop.setStyleSheet("QLabel  {background:  url(\":/images/loop_h.png\") }")


    #private EVENTS ...
    #СОБЫТИЯ Главного окна

    def closeEvent(self, event):
        self.saveSets()
        super().closeEvent(event)

    def dropEvent(self, event):
        control = (event.keyboardModifiers() & QtCore.Qt.ControlModifier) == QtCore.Qt.ControlModifier

        if not control: self.model.clear()

        filelist = []
        for url in event.mimeData().urls():
            fn = url.fileName()
            if self.isMusic(fn):
                self.model.appendRow(QtGui.QStandardItem(QtGui.QIcon(":/images/playlist_icon.png"), fn))
                filelist.append(url.toLocalFile())
        self.player.addFiles(filelist, not control)
        self.savePlayList()
        if not control and self.model.rowCount() > 0:
            self.player.playByIndex(0)
            #self.ui.listView.clearSelection()
            #self.ui.listView.selectionModel().select(self.model.index(0,0), QtGui.QItemSelectionModel.Toggle)
        event.acceptProposedAction()
        self.savePlayList()


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.acceptProposedAction()

    #private ...
    #Прочие процедуры и функции

    def checkargv(self):
        filenames = []
        fname = ''
        for fn in sys.argv[1:]:
            fdir = fn
            if os.path.isfile(fn):
                fdir = os.path.dirname(fn)
                fname = fn
            elif not os.path.isdir(fn): continue
            files = os.listdir(fdir)
            for f in files:
                if self.isMusic(f):
                    filenames.append(os.path.join(fdir,f))

        if len(filenames) > 0:
            for fn in filenames:
                self.model.appendRow(QtGui.QStandardItem(QtGui.QIcon(":/images/playlist_icon.png"), os.path.basename(fn)))
            self.player.addFiles(filenames, True)
            index = 0
            if len(fname) > 0:
                index = filenames.index(fname)
            self.player.playByIndex(index)
            if index > 0:
                self.ui.listView.scrollTo(self.model.index(index,0))
        else:
            self.loadPlayList()


    def createSlider(self):
        self.slider = MSlider()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(0)
        self.slider.fitHeight = True
        self.slider.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.slider)
        self.ui.w_track.setLayout(layout)

    def createVolumeControl(self):
        vol = MVolume()
        vol.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        vol.beginUpdate()
        vol.setKnobBgImage(QtGui.QPixmap(":/images/knob_bg.png"))
        vol.setKnobImage(QtGui.QPixmap(":/images/knob_ind.png"))
        vol.setPos(100)
        layout = QtWidgets.QHBoxLayout(self.ui.w_volume)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(vol)
        vol.endUpdate()
        self.vol = vol


    def isMusic(self, fn):
        ext = fn[-4:].lower()
        return ext == ".mp3" or ext == ".wma" or  ext == ".wav" or  ext == ".m4a"

    #def keyPressEvent(self, event):
    #    print(event.key())

    def loadPlayList(self):
        if self.ui.comboBox.count() == 0 or self.ui.comboBox.currentIndex() < 1:
            fn = os.path.join(self.path, 'default.plt')
        else:
            fn = os.path.join(self.path, self.ui.comboBox.itemText(self.ui.comboBox.currentIndex())+'.plt')
        self.model.clear()
        self.player.playlist.clear()
        if not os.path.isfile(fn): return
        filenames = []
        with open(fn,'r') as f:
            for filename in f:
                filename = filename.rstrip('\n')
                filenames.append(filename)
                self.model.appendRow(QtGui.QStandardItem(QtGui.QIcon(":/images/playlist_icon.png"), os.path.basename(filename)))
        self.player.addFiles(filenames)


    def savePlayList(self):
        if self.ui.comboBox.count() == 0 or self.ui.comboBox.currentIndex() < 1:
            fn = os.path.join(self.path, 'default.plt')
        else:
            fn = os.path.join(self.path, self.ui.comboBox.itemText(self.ui.comboBox.currentIndex())+'.plt')

        if len(self.player.playlist) == 0:
            open(fn, 'w').close()
            return
        with open(fn,'w') as f:
            for filename in self.player.playlist:
                f.write(filename+'\n')

    def saveSets(self):
        set = QtCore.QSettings(os.path.join('RoganovSoft', 'AudioPlayer'), "config")
        p = self.pos()
        set.setValue("Main/left",p.x())
        set.setValue("Main/top",p.y())
        set.setValue("Main/width",self.width())
        set.setValue("Main/height",self.height())
        set.setValue("AUDIO/volume", self.vol.position)
        if self.ui.comboBox.currentIndex() < 1:
            set.setValue("AUDIO/playlist","")
        else:
            set.setValue("AUDIO/playlist",self.ui.comboBox.itemText(self.ui.comboBox.currentIndex()))



    def loadSets(self):
        set = QtCore.QSettings(os.path.join('RoganovSoft', 'AudioPlayer'), "config")
        x = int(set.value("Main/left",0))
        y = int(set.value("Main/top",0))
        w = int(set.value("Main/width",0))
        h = int(set.value("Main/height",0))
        if x != 0 and y != 0:
            self.move(x,y)
        if w != 0 and h != 0:
            self.resize(w,h)
        self.vol.setPos(int(set.value("AUDIO/volume", self.vol.position)))
        self.player.set_volume(self.vol.position)
        pl = set.value("AUDIO/playlist","")
        if len(pl) > 0 and self.model.rowCount() == 0:
            for i in range(1, self.ui.comboBox.count()):
                if pl == self.ui.comboBox.itemText(i):
                    self.ui.comboBox.setCurrentIndex(i)
                    self.loadPlayList()
                    break


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/images/logo.png"))
    main = AudioPlayer(app)
    app.mainwindow = main
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
