#!/usr/bin/python3
'''
Audio player using lib bass and pyqt5
Author Roganov G.V. roganovg@mail.ru
'''

import sys
import os
from PyQt5 import QtGui, QtCore,QtWidgets
from mainwindow import Ui_MainWindow, labelstyle
from mvolume import MVolume


#set current directory for bass library
os.chdir(os.path.dirname(os.path.realpath(__file__)))
from BASSPlayer import BassPlayer, PlayMode_Playing, PlayMode_Paused
from mslider import MSlider
from equalizer import Equalizer
from server import DGramServer, send #StreamServer

#for one application instance only
class Application(QtWidgets.QApplication):
    def __init__(self, argv):
        super(Application, self).__init__(argv)
        self._singular = QtCore.QSharedMemory("SharedMemoryForOnlyOneInstanceOfAudioPlayer", self)

    def lock(self):
        if self._singular.attach(QtCore.QSharedMemory.ReadOnly):
            self._singular.detach()
            return False
        if self._singular.create(1):
            return True

        return False

    def __del__(self):
        if self._singular != None:
            if self._singular.isAttached():
                self._singular.detach()


def secondsToTime(s):
    m = s // 60
    h = m // 60
    m %= 60
    s %= 60
    return f'{h:02d}:{m:02d}:{s:02d}' if h > 0 else f'{m:02d}:{s:02d}'

class AudioPlayer(QtWidgets.QMainWindow):
    LOOP_OFF = 0
    LOOP_TOEND = 1
    LOOP_REPEAT = 2
    #Создание окна
    def __init__(self, parent=None):
        super(AudioPlayer, self).__init__(None)
        #создание основных контролов и лейаутов происходит в классе Ui_MainWindow модуля mainwindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        set = QtCore.QSettings(os.path.join('RoganovSoft', 'AudioPlayer'), "config")
        self.path = os.path.dirname(set.fileName())
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        #cоздаю свой контрол управления громкостью
        self.createVolumeControl()
        #контрол управления временем/позицией
        self.createSlider()
        #класс BassPlayer управляет воспроизведением и вызовами к BASS
        self.player = BassPlayer()
        self.model = QtGui.QStandardItemModel(self)
        self.ui.listView.setModel(self.model)
        #разрешаем перетаскивание на форму
        self.setAcceptDrops(True)
        self.loop = self.LOOP_OFF
        #грузим сохранённый еквалайзер
        set.beginGroup('equalizer_gains')
        for i in range(self.player.eqbandcount):
            self.player.EQBands[i].Gain = int(set.value(f'band_{i}','0'))
        set.endGroup()

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
        self.vol.setPos(self.player.get_volume())
        #грузим настройки
        self.loadSets(set)

        self.read_attr_buffer = []
        self.read_attr_ontime = False

        self.eqdialog = None
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.onTimer)
        self.timer.start()

        self.vistimer = QtCore.QTimer(self)
        self.vistimer.setInterval(33)
        self.vistimer.timeout.connect(self.onVisTimer)
        self.vistimer.start()
        self.runserver()

    #Необходим для приёма данных от вторичных запущенных экземпляров приложений
    #Когда ассоциируем аудио файлы с этим приложением.
    def runserver(self):
        thread = QtCore.QThread()
        self.serv = DGramServer(thread) #StreamServer(thread)
        self.serv.onFinish.connect(self.serverThreadFinish)
        self.serv.onRead.connect(self.doRead)
        self.serv.moveToThread(thread)
        thread.started.connect(self.serv.run)
        thread.start()

    def serverThreadFinish(self, msg):
        print('server thread finished')


    def read_timer(self):
        self.read_attr_ontime = False

        filenames = []
        files = []
        files_count = 0
        filename = ''
        def add_dir(fdir, lst):
            mfiles = os.listdir(fdir)
            for f in mfiles:
                if self.isMusic(f):
                    lst.append(os.path.join(fdir,f))


        if len(self.read_attr_buffer)>0:
            if self.read_attr_buffer[0].lower() == '-s':
                self.player.stop()
            elif self.read_attr_buffer[0].lower() == '-p':
                if self.model.rowCount() == 0:
                    if self.ui.comboBox.count() > 1:
                        self.ui.comboBox.setCurrentIndex(1)
                        self.loadPlayList()

                self.player.play_pause()
            elif self.read_attr_buffer[0].lower() == '-n':
                pass
            elif self.read_attr_buffer[0].lower() == '-vs':
                self.player.set_volume(30)
            elif self.read_attr_buffer[0].lower() == '-vl':
                self.player.set_volume(94)

            for a in self.read_attr_buffer:
                if os.path.isfile(a) or os.path.isdir(a):
                    files.append(a)

            files_count = len(files)

            for f in files:
                if os.path.isfile(f):
                    if filename == '': filename = f
                    if files_count > 1:
                        if self.isMusic(f):
                            filenames.append(f)
                    else:
                        add_dir(os.path.dirname(f), filenames)
                else:
                    add_dir(f, filenames)

            if filename == '' and len(filenames) > 0:
                filename = filenames[0]


            if len(filenames) > 0:
                self.ui.comboBox.setCurrentIndex(0)
                self.clearPlayList()

                for fn in filenames:
                    item = QtGui.QStandardItem(QtGui.QIcon(":/images/playlist_icon.png"), os.path.basename(fn))
                    item.fn = fn
                    self.model.appendRow(item)
                #self.player.addFiles(filenames, True)
                index = 0
                if len(filename) > 0:
                    index = filenames.index(filename)
                #self.player.playByIndex(index)
                fn = self.model.item(index).fn
                if self.player.load(fn):
                    self.player.play()
                    self.ui.l_info.setText(os.path.basename(self.player.currentfilename))
                    self.onPlayerPlaylistIndexChanged(index)
                if index > 0:
                    self.ui.listView.scrollTo(self.model.index(index,0))

        self.read_attr_buffer = []

    def doRead(self, data):
        attr = data.split('\n')
        if self.read_attr_ontime:
            self.read_attr_buffer += attr
        else:
            self.read_attr_buffer = attr
            self.read_attr_ontime = True
            QtCore.QTimer.singleShot(900, self.read_timer)

    

    #связываем события со слотами
    def setEvent(self):
        self.player.status_changed.connect(self.onPlayerStateChanged)
        self.player.stream_finished.connect(self.onPlayerStreamFinish)
        #self.player.volumeChanged.connect(self.vol.setPos)
        #self.player.positionChanged.connect(self.playerPosChanged)
        #self.player.playlistIndexChanged.connect(self.onPlayerPlaylistIndexChanged)
        #self.player.playingFileChanged.connect(self.onPlayerFileChanged)
        self.vol.posChanged.connect(self.player.set_volume)
        self.slider.posChanged.connect(self.onSliderPosChanged)

        self.ui.listView.doubleClicked.connect(self.listviewdoubleClicked)
        self.ui.lPlay.onClick.connect(self.player.play_pause)
        self.ui.lStop.onClick.connect(self.player.stop)
        self.ui.lPrev.onClick.connect(self.prev)
        self.ui.lNext.onClick.connect(self.next)
        self.ui.lLoop.onClick.connect(self.setLoop)
        self.ui.l_delfile.onClick.connect(self.delFromPlayList)
        self.ui.l_clearplaylist.onClick.connect(self.clearPlayList)
        self.ui.l_addfile.onClick.connect(self.addFilePlayList)
        self.ui.l_addplaylist.onClick.connect(self.addPlayList)
        self.ui.l_delplaylist.onClick.connect(self.delPlayList)
        self.ui.l_editplaylist.onClick.connect(self.editPlayList)
        self.ui.lEq.onClick.connect(self.eqClick)
        self.ui.comboBox.activated.connect(self.comboBoxActivated)
        self.ui.lclose.onClick.connect(self.close)

        #регистрируем класс QAction исключительно для shortcut -  пробел для вызова паузы или плей
        # но вероятнее всего это не работает. т.к. фокус перехватывается контролами ComboBox(список плейлистов) и listView(плейлист)
        #в связи с этим я переопределил эти компоненты см. модуль mywidgets классы MyComboBox и MyListView
        self.ui.comboBox.keyPressed.connect(self.controlKeyPressed)
        self.ui.listView.keyPressed.connect(self.controlKeyPressed)

        self.actionPlayPause = QtWidgets.QAction(self)
        self.actionPlayPause.setObjectName("actionPlayPause")
        self.actionPlayPause.setShortcut("Space")
        self.actionPlayPause.triggered.connect(self.player.play_pause)


    def onTimer(self):
        if self.player.PlayerMode == PlayMode_Playing:
            s_pos, s_max = self.player.get_position(), self.player.get_length()
            self.timeChange(s_pos, s_max)
            self.slider.posChange(round(s_pos/s_max*1000))
        elif self.player.PlayerMode == PlayMode_Paused:
            pass
        else:
            self.ui.l_time.setText('0.00/0.00')
            self.slider.posChange(0)

    #private slots...
    #ОБРАТНЫЕ вызовы от плеера .....

    def onPlayerStateChanged(self):
        state = self.player.PlayerMode
        if state < 3:
            self.ui.state_icon.setPixmap(QtGui.QPixmap(':/images/stop_state.png'))
            self.slider.posChange(0)
            self.ui.l_time.setText('0.00/0.00')
        elif state == 3:
            self.ui.state_icon.setPixmap(QtGui.QPixmap(':/images/play_state.png'))
        elif state == 4:
            self.ui.state_icon.setPixmap(QtGui.QPixmap(':/images/pause_state.png'))

        if state == 3:
            self.ui.lPlay.styles = {'default':labelstyle([':/images/pause.png', ':/images/pause_over.png']), 'pressed':labelstyle([':/images/pause_down.png'])}
        else:
            self.ui.lPlay.styles = {'default':labelstyle([':/images/play.png', ':/images/play_over.png']), 'pressed':labelstyle([':/images/play_down.png'])}
        self.ui.lPlay.updatestyle()


    def next(self):
        if self.model.rowCount() < 2: return
        if len(self.ui.listView.selectedIndexes()) > 0:
            i = self.ui.listView.selectedIndexes()[0].row()
        else:
            i = 0
        i += 1
        if  i >= self.model.rowCount():
            i = 0
        fn = self.model.item(i).fn
        if self.player.load(fn):
            self.player.play()
            self.ui.l_info.setText(os.path.basename(self.player.currentfilename))
            self.onPlayerPlaylistIndexChanged(i)

    def prev(self):
        if self.model.rowCount() < 2: return
        if len(self.ui.listView.selectedIndexes()) > 0:
            i = self.ui.listView.selectedIndexes()[0].row()
        else:
            i = 0
        i -= 1
        if  i < 0:
            i = self.model.rowCount()-1
        fn = self.model.item(i).fn
        if self.player.load(fn):
            self.player.play()
            self.ui.l_info.setText(os.path.basename(self.player.currentfilename))
            self.onPlayerPlaylistIndexChanged(i)

    def onPlayerStreamFinish(self):
        if self.loop == self.LOOP_OFF:
            self.player.stop()
            return
        if len(self.ui.listView.selectedIndexes()) > 0:
            i = self.ui.listView.selectedIndexes()[0].row()
        else:
            i = 0
        if self.loop == self.LOOP_TOEND:
            if i < self.model.rowCount() -1:
                self.next()
            else:
                self.player.stop()
        else:
            self.next()


    def onPlayerPlaylistIndexChanged(self, index):
        self.ui.listView.clearSelection()
        self.ui.listView.selectionModel().select(self.model.index(index,0), QtCore.QItemSelectionModel.Toggle)
        self.ui.listView.update()


    #Прочие методы событий.......

    def onSliderPosChanged(self, pos):
        if self.player.PlayerMode == PlayMode_Playing:
            s_max = self.player.get_length()
            if s_max == 0: return
            pos = round(pos/1000*s_max)
            self.player.set_position(pos)
            self.timeChange(pos, s_max)

    def timeChange(self, s_pos, s_max):
        self.ui.l_time.setText(secondsToTime(s_pos)+' / '+secondsToTime(s_max))

    def listviewdoubleClicked(self, index):
        if index.row() < 0: return
        fn = self.model.item(index.row()).fn
        if self.player.load(fn):
            self.player.play()
            self.ui.l_info.setText(os.path.basename(self.player.currentfilename))
            self.onPlayerPlaylistIndexChanged(index.row())

    def delFromPlayList(self):
        if self.model.rowCount() == 0: return
        i =  self.ui.listView.currentIndex().row()
        if i < 0: return
        self.model.removeRow(i)
        self.savePlayList()
        pass

    def clearPlayList(self):
        if self.model.rowCount() == 0: return
        self.model.clear()
        self.savePlayList()

    def addFilePlayList(self):
        exts = self.player.exts.replace('.', ' *.')
        exts = f'MUSIC ({exts})'
        filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Выбор файла...", filter=exts)
        if not filenames: return
        #self.player.addFiles(filenames)
        for fn in filenames:
            item = QtGui.QStandardItem(QtGui.QIcon(":/images/playlist_icon.png"), os.path.basename(fn))
            item.fn = fn
            self.model.appendRow(item)

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
            self.eqdialog = Equalizer(self.player)
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
            if self.model.rowCount() == 0: return
            i =  self.ui.listView.currentIndex().row()
            if i < 0: return
            for index in self.ui.listView.selectedIndexes():
                if i == index.row(): return

            fn = self.model.item(i).fn
            if self.player.load(fn):
                self.player.play()
                self.ui.l_info.setText(os.path.basename(self.player.currentfilename))
                self.onPlayerPlaylistIndexChanged(i)




    def setLoop(self, default=None):
        if default != None:
            self.loop = default
        else:
            if self.loop == self.LOOP_TOEND:
                self.loop = self.LOOP_REPEAT
            elif self.loop == self.LOOP_OFF:
                self.loop = self.LOOP_TOEND
            else:
                self.loop = self.LOOP_OFF

        if self.loop == self.LOOP_OFF:
            self.ui.lLoop.styles['default'] = 'QLabel  {background:  url(":/images/loop_off.png") } QLabel:hover {background:  url(":/images/loop_off_over.png")}'
        elif self.loop == self.LOOP_TOEND:
            self.ui.lLoop.styles['default'] = 'QLabel  {background:  url(":/images/loop_down.png") } QLabel:hover {background:  url(":/images/loop_down_over.png")}'
        else:
            self.ui.lLoop.styles['default'] = 'QLabel  {background:  url(":/images/loop_on.png") } QLabel:hover {background:  url(":/images/loop_on_over.png")}'


    #private EVENTS ...
    #СОБЫТИЯ Главного окна

    def closeEvent(self, event):
        self.serv.keep_running = False
        self.saveSets()
        super().closeEvent(event)

    def dropEvent(self, event):
        control = (event.keyboardModifiers() & QtCore.Qt.ControlModifier) == QtCore.Qt.ControlModifier

        if not control: self.model.clear()

        for url in event.mimeData().urls():
            fn = url.toLocalFile()
            if self.isMusic(fn):
                item = QtGui.QStandardItem(QtGui.QIcon(":/images/playlist_icon.png"), os.path.basename(fn))
                item.fn = fn
                self.model.appendRow(item)

        #self.player.addFiles(filelist, not control)
        self.savePlayList()
        if not control and self.model.rowCount() > 0:
            fn = self.model.item(0).fn
            if self.player.load(fn):
                self.player.play()
                self.ui.l_info.setText(os.path.basename(self.player.currentfilename))
                self.onPlayerPlaylistIndexChanged(0)

        event.acceptProposedAction()


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.acceptProposedAction()

    #private ...
    #Прочие процедуры и функции

    def checkargv(self):
        filenames = []
        fname = ''
        if len(sys.argv) == 1:
            return
        cmd = sys.argv[1].lower()
        if cmd  == '-p':
            if self.model.rowCount() == 0:
                if self.ui.comboBox.count() > 1:
                    self.ui.comboBox.setCurrentIndex(1)
                    self.loadPlayList()
            self.player.play_pause()
            return
        elif cmd == '-s':
            self.player.stop()
            return
        elif cmd == '-n':
            #self.player.next()
            return

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
                item = QtGui.QStandardItem(QtGui.QIcon(":/images/playlist_icon.png"), os.path.basename(fn))
                item.fn = fn
                self.model.appendRow(item)
            #self.player.addFiles(filenames, True)
            index = 0
            if len(fname) > 0:
                index = filenames.index(fname)
            #self.player.playByIndex(index)
            fn = self.model.item(index).fn
            if self.player.load(fn):
                self.player.play()
                self.ui.l_info.setText(os.path.basename(self.player.currentfilename))
                self.onPlayerPlaylistIndexChanged(index)
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
        return ext in self.player.exts

    def loadPlayList(self):
        if self.ui.comboBox.count() == 0 or self.ui.comboBox.currentIndex() < 1:
            fn = os.path.join(self.path, 'default.plt')
        else:
            fn = os.path.join(self.path, self.ui.comboBox.itemText(self.ui.comboBox.currentIndex())+'.plt')
        self.model.clear()
        #self.player.playlist.clear()
        if not os.path.isfile(fn): return
        filenames = []
        with open(fn,'r') as f:
            for filename in f:
                filename = filename.rstrip('\n')
                filenames.append(filename)
                item = QtGui.QStandardItem(QtGui.QIcon(":/images/playlist_icon.png"), os.path.basename(filename))
                item.fn = filename
                self.model.appendRow(item)
        #self.player.addFiles(filenames)


    def savePlayList(self):
        if self.ui.comboBox.count() == 0 or self.ui.comboBox.currentIndex() < 1:
            fn = os.path.join(self.path, 'default.plt')
        else:
            fn = os.path.join(self.path, self.ui.comboBox.itemText(self.ui.comboBox.currentIndex())+'.plt')

        if self.model.rowCount() == 0:
            open(fn, 'w').close()
            return
        with open(fn,'w') as f:
            for i in range(self.model.rowCount()):
                fn = self.model.item(i).fn
                f.write(fn+'\n')

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
        set.beginGroup('equalizer_gains')
        for i in range(self.player.eqbandcount):
            set.setValue(f'band_{i}',self.player.EQBands[i].Gain)
        set.endGroup()
        set.setValue("General/EQ_enabled", self.player.EqualizerEnabled)
        set.setValue("General/Loop", self.loop)

    def loadSets(self, set):

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
        self.player.EqualizerEnabled = set.value("General/EQ_enabled","true") == "true"
        self.loop = int(set.value("General/Loop", self.loop))
        if self.loop == self.LOOP_TOEND:
            self.ui.lLoop.styles = {'default':labelstyle([':/images/loop_down.png',':/images/loop_down_over.png'])}
            self.ui.lLoop.setStyleSheet(self.ui.lLoop.styles['default'])
        elif self.loop == self.LOOP_REPEAT:
            self.ui.lLoop.styles = {'default':labelstyle([':/images/loop_on.png',':/images/loop_on_over.png'])}
            self.ui.lLoop.setStyleSheet(self.ui.lLoop.styles['default'])

        pl = set.value("AUDIO/playlist","")
        if len(pl) > 0 and self.model.rowCount() == 0:
            for i in range(1, self.ui.comboBox.count()):
                if pl == self.ui.comboBox.itemText(i):
                    self.ui.comboBox.setCurrentIndex(i)
                    self.loadPlayList()
                    break

    def onVisTimer(self):
        self.player.get_fftdata()
        self.ui.viswidget.updatefft(self.player.fftbands, self.player.zerofft)


def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = Application(sys.argv)
    if not app.lock():
        if len(sys.argv) > 1:
            send('\n'.join(sys.argv[1:]))
        return -42;
    app.setWindowIcon(QtGui.QIcon(":/images/logo.png"))
    main = AudioPlayer(app)
    app.mainwindow = main
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
