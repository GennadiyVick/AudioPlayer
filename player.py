import platform
import os
import sys
import vlc
from PyQt5 import QtCore
#этот код надо оптимизировать, здесь есть над чем поработать
class Player(QtCore.QObject):
    #статические параметры
    STATE_STOP  = 0
    STATE_PLAY  = 1
    STATE_PAUSE = 2
    LOOP_TOEND = 0
    LOOP_REPEAT = 1
    #сигналы
    stateChanged = QtCore.pyqtSignal(int)
    volumeChanged = QtCore.pyqtSignal(int)
    positionChanged = QtCore.pyqtSignal(int)
    playlistIndexChanged = QtCore.pyqtSignal(int)
    playingFileChanged = QtCore.pyqtSignal()

    #конструктор
    def __init__(self, maxpos = 1000):
        #maxpos это максимальная позиция контрола управления временем/позицией
        super(Player, self).__init__()
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        self.media = None
        self.state = self.STATE_STOP
        self.maxpos = maxpos
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.onTimer)
        self.playlist = []
        self.currentIndex = -1
        self.volume = 100
        self.pos = 0
        self.duration = 0
        self.loop = self.LOOP_TOEND
        self.equalizer = None
        #Получаем количество полос эквалайзера, однако не всякое железо поддерживает это количество,
        #например на домашнем компе все полосы работали нормально, на рабочем только первые 6.
        #Первый слидер(или полоса) это предусиление поэтому  +1
        self.bandcount = vlc.libvlc_audio_equalizer_get_band_count()+1
        set = QtCore.QSettings(os.path.join('RoganovSoft', 'AudioPlayer'), "config")
        self.custompreset = [int(set.value(f"EQ_customPreset_{i}", 20)) for i in range(self.bandcount)]
        self.presetname = set.value("EQ_preset","custom")
        self.equalizerenabled = set.value("EQ_enabled",'False') == 'True'
        self.presets = []
        for i in range(vlc.libvlc_audio_equalizer_get_preset_count()):
            self.presets.append(vlc.libvlc_audio_equalizer_get_preset_name(i).decode())

        if self.presetname == 'custom':
            self.equalizer = vlc.libvlc_audio_equalizer_new()
            self.equalizer.set_preamp(self.custompreset[0]-20)
            for i in range(1,self.bandcount):
                self.equalizer.set_amp_at_index(self.custompreset[i]-20,i-1)
            if self.equalizerenabled:
                self.mediaplayer.set_equalizer(self.equalizer)
        else:
            if self.presetname in self.presets:
                i = self.presets.index(self.presetname)
                self.equalizer = vlc.libvlc_audio_equalizer_new_from_preset(i)
                if self.equalizerenabled:
                    self.mediaplayer.set_equalizer(self.equalizer)


    def play_pause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.state = self.STATE_PAUSE
            self.stateChanged.emit(self.state)
            self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.playCurrent()
                return

            self.state = self.STATE_PLAY
            self.stateChanged.emit(self.state)
            self.timer.start()

    def stop(self):
        self.mediaplayer.stop()
        self.timer.stop()
        self.duration = 0
        if self.state != self.STATE_STOP:
            self.state = self.STATE_STOP
            self.stateChanged.emit(self.state)


    def playCurrent(self):
        l = len(self.playlist)
        if l == 0: return
        if self.currentIndex < 0 or self.currentIndex >= l:
            self.currentIndex = 0
            self.playlistIndexChanged.emit(self.currentIndex)
        self.playfile(self.playlist[self.currentIndex])

    def next(self):
        l = len(self.playlist)
        if l == 0: return
        self.currentIndex += 1
        if self.currentIndex >= l:
            self.currentIndex = 0
        self.playfile(self.playlist[self.currentIndex])
        self.playlistIndexChanged.emit(self.currentIndex)

    def prev(self):
        l = len(self.playlist)
        if l == 0: return
        self.currentIndex -= 1
        if self.currentIndex < 0:
            self.currentIndex = l-1
        self.playfile(self.playlist[self.currentIndex])
        self.playlistIndexChanged.emit(self.currentIndex)

    def play(self, fn, clearPlayList = False):
        if clearPlayList:
            self.playlist.clear()
        self.playlist.append(fn)
        self.currentIndex = len(self.playlist)-1
        self.playfile(self.playlist[self.currentIndex])
        self.playlistIndexChanged.emit(self.currentIndex)

    def playByIndex(self, index):
        self.currentIndex = index
        if index < 0:
            if len(self.playlist) > 0:
                self.currentIndex = 0
            else:
                return
        elif index >= len(self.playlist):
            self.currentIndex = 0
        self.playfile(self.playlist[self.currentIndex])
        self.playlistIndexChanged.emit(self.currentIndex)

    def addFiles(self, files, clearPlayList = False):
        if clearPlayList:
            self.playlist.clear()
        self.playlist.extend(files)

    def playfile(self, fn):
        if fn == None or not os.path.isfile(fn):
            self.stop()
            return
        if self.media != None:
            vlc.libvlc_media_release(self.media)
        self.media = self.instance.media_new(fn)
        self.mediaplayer.set_media(self.media)
        self.media.parse() #for getInfo
        self.play_pause()
        #Громкость всегда сбрасывается при создании нового media
        self.mediaplayer.audio_set_volume(self.volume)
        self.duration = self.getLength()
        self.playingFileChanged.emit()

    def getCurrentInfo(self):
        if len(self.playlist) == 0 or self.currentIndex < 0 or self.media == None: return None
        return {'filename': self.playlist[self.currentIndex],'title':self.media.get_meta(vlc.Meta.Title),'album':self.media.get_meta(vlc.Meta.Album),'artist':self.media.get_meta(vlc.Meta.Artist)}

    def set_volume(self, volume):
        self.volume = volume
        self.mediaplayer.audio_set_volume(volume)

    def set_position(self, pos):
        if self.state == self.STATE_STOP: return
        self.pos = pos
        self.timer.stop()
        self.mediaplayer.set_position(pos / self.maxpos)
        self.timer.start()

    def onTimer(self):
        v = self.mediaplayer.audio_get_volume()
        if v != -1 and v != self.volume:
            self.volume = v
            self.volumeChanged.emit(v)
        #self.mediaplayer.get_position() =  от 0 до 1
        p = int(self.mediaplayer.get_position() * self.maxpos)
        if p < 0: p = 0
        if p != self.pos:
            self.pos = p
            self.positionChanged.emit(p)

        if not self.mediaplayer.is_playing():
            self.timer.stop()
            if self.state == self.STATE_PLAY:
                self.stop()
                l = len(self.playlist)
                if l > 0 and (self.currentIndex < l-1 or self.loop == self.LOOP_REPEAT):
                    self.next()
                #self.finished.emit()

    def getLength(self):
        return 0 if self.state == self.STATE_STOP else vlc.libvlc_media_get_duration(self.media)

    def msecondsToTime(self, ms):
        s = ms // 1000
        m = s // 60
        h = m // 60
        m %= 60
        s %= 60
        return f'{h:02d}:{m:02d}:{s:02d}' if h > 0 else f'{m:02d}:{s:02d}'

    def getTimePos(self):
        if self.state == self.STATE_STOP or self.pos == 0:
            return '0.00'
        msec = round(self.pos / self.maxpos * self.duration)
        return self.msecondsToTime(msec)

    def getTimeDuration(self):
        if self.state == self.STATE_STOP or self.duration == 0:
            return '0.00'
        return self.msecondsToTime(self.duration)

    def getBandCount(self):
        vlc.libvlc_audio_equalizer_set_amp_at_index(self.equalizer, 18.5, 8)
        return vlc.libvlc_audio_equalizer_get_band_count()

