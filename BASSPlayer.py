from bass.pybass import *
#from bass import pytags
import ctypes
from signal import Signal
import platform
import os
from math import sqrt
"""
Author Roganov G.V. roganovg@mail.ru
"""

avial_exts = ''
NumFFTBands = 44
NumEQBands = 10
#EQBandWidth = [3, 4, 4, 4, 5, 6, 5, 4, 3, 3]
#EQFreq = [80, 160, 320, 600, 1000, 3000, 6000, 10000, 12000, 14000]
EQBandWidth = [6, 8, 14,  18,  21,  24,  28,   36,   44,   52]
EQFreq      = [44, 80, 200, 400, 800, 1600, 3000, 6000, 10000, 14000]

PlayMode_Standby = 0
PlayMode_Ready = 1
PlayMode_Stopped = 2
PlayMode_Playing = 3
PlayMode_Paused = 4
Channel_NotOpened = 0
Channel_Stream = 1
Channel_Internet = 2
Channel_Plugin = 3
player_instance = None
SPEC_WIDTH = 200
FLOAT_SIZE = 4
CALC_FFT = 10.0 / (NumFFTBands - 1)


# lib name to file name regardless of OS type
def crpl_libname(fn):
    if platform.system().lower() == 'windows':
        return f'{fn}.dll'
    else:
        return f'lib{fn}.so'


class Library():
    def __init__(self, exts):
        self.exts = exts
        self.enabled = False

    def load(self, fn, ext):
        return None


class BassLibrary(Library):
    def __init__(self):
        super(BassLibrary, self).__init__('.mp3.wav.ogg.mpga')
        self.enabled = True

    def load(self, fn, ext):
        return BASS_StreamCreateFile(False, fn, 0, 0, 0)


class AC3Library(Library):
    def __init__(self):
        super(AC3Library, self).__init__('.ac3')
        if os.path.isfile(crpl_libname('bass_ac3')):
            try:
                from bass import pybass_ac3
            except Exception as e:
                print('bass_ac3 library not exists', str(e))
            else:
                self.enabled = True
                self.ac3 = pybass_ac3

    def load(self, fn, ext):
        if self.enabled:
            return self.ac3.BASS_AC3_StreamCreateFile(False, fn, 0, 0, 0)
        else:
            return None


class ACCLibrary(Library):
    def __init__(self):
        super(ACCLibrary, self).__init__('.aac.m4a.m4p')
        if os.path.isfile(crpl_libname('bass_aac')):
            try:
                from bass import pybass_aac
            except:
                print('bass_aac library not exists')
            else:
                self.enabled = True
                self.aac = pybass_aac
        else:
            print('bass_aac lib not found')

    def load(self, fn, ext):
        if not self.enabled:
            return None
        if ext == '.aac':
            return self.aac.BASS_AAC_StreamCreateFile(False, fn, 0, 0, 0)
        else:
            return self.aac.BASS_MP4_StreamCreateFile(False, fn, 0, 0, 0)


class WMALibrary(Library):
    def __init__(self):
        super(WMALibrary, self).__init__('.wma')
        if os.path.isfile(crpl_libname('basswma')):
            try:
                from bass import pybasswma
            except:
                print('basswma library not exists')
            else:
                self.enabled = True
                self.wma = pybasswma

    def load(self, fn, ext):
        return self.wma.BASS_WMA_StreamCreateFile(False, fn, 0, 0, 0)


#DOWNLOADPROC = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong)
#DOWNLOADPROC = func_type(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.c_void_p)

def download_callback(buffer, length, downloaded, user):
    print(f"Загружено: {downloaded} байт из {length}")


callback = DOWNLOADPROC(download_callback)


class Libraries(list):
    def __init__(self):
        super(Libraries, self).__init__()
        self.append(BassLibrary())
        print('Libraries init')
        global avial_exts
        acclib = ACCLibrary()
        if acclib.enabled:
            self.append(acclib)
        self.append(AC3Library())
        if platform.system().lower() == 'windows':
            self.append(WMALibrary())

        for lib in self:
            if lib.enabled:
                avial_exts += lib.exts

    def load(self, fn, ext):
        for lib in self:
            if lib.enabled and ext in lib.exts:
                return lib.load(fn, ext)
        return 0

    def load_url(self, url):
        return BASS_StreamCreateURL(ctypes.c_char_p(url.encode('utf-8')), 0, 0, DOWNLOADPROC(0), 0)


class BandData:
    def __init__(self, CenterFreq=0.0, Bandwidth=0.0, Gain=0):
        self.CenterFreq = CenterFreq
        self.Bandwidth = Bandwidth
        self.Gain = Gain

'''
proxy_ptr = ctypes.c_char_p("http://10.51.248.2:8080".encode())
proxy_address = ctypes.cast(proxy_ptr, ctypes.POINTER(ctypes.c_void_p)).contents.value
if BASS_SetConfig(BASS_CONFIG_NET_PROXY, proxy_address):
    print('proxy set ok')
else:
    print(f'proxy not set {BASS_ErrorGetCode()}')
'''
'''
if BassLoaded:
    proxy_str = "http://10.51.248.2:8080"
    proxy_ptr = ctypes.c_char_p(proxy_str.encode('utf-8'))

    if BASS_SetConfigPtr(BASS_CONFIG_NET_PROXY, proxy_ptr):
        print('proxy set ok')
    else:
        error_code = BASS_ErrorGetCode()
        print(f'proxy not set, error code: {error_code}')
'''


def get_devices():
    devices = []
    device_count = 0
    while True:
        info = BASS_DEVICEINFO()
        if not BASS_GetDeviceInfo(device_count, info):
            break
        if info.flags & BASS_DEVICE_ENABLED:
            devices.append((device_count, info.name.decode()))
        device_count += 1
    return devices


class BassPlayer:
    def __init__(self):
        global player_instance
        player_instance = self
        self.ChannelType = Channel_NotOpened
        self.Channel = 0
        self.eqbandcount = NumEQBands
        self.BassLoaded = BASS_Init(-1, 44100, 0, 0, 0)
        self.libraries = Libraries()
        self.BassInfoParam = BASS_INFO()
        self.EqualizerEnabled = False
        self.EQHandle = [0 for i in range(NumEQBands)]
        self.EQBands = [BandData(EQFreq[i], EQBandWidth[i]) for i in range(NumEQBands)]
        self.fftbands = [0 for i in range(NumFFTBands)]
        self.exts = ''
        self.lasterror = ''
        self.status_changed = Signal()
        self.stream_finished = Signal()
        self.PlayerMode = PlayMode_Standby
        self.currentfilename = ''
        self.volume = 100
        self.fft_limits = []
        b0 = 0
        for i in range(NumFFTBands):
            b1 = round(2 ** (i * CALC_FFT))
            if b1 > 1023: b1 = 1023
            if b1 <= b0: b1 = b0 + 1
            self.fft_limits.append((b0, b1))
            b0 = b1
        self.zerofft = False
        self.tfftdata = ctypes.c_float * 1024
        self.spec_size = SPEC_WIDTH * 2 * 4
        self.tspecdata = ctypes.c_float * SPEC_WIDTH * 2
        self.exts = avial_exts

    def __del__(self):
        if self.BassLoaded:
            BASS_Free()

    def load(self, fn):
        if not self.BassLoaded:
            self.lasterror = 'BASS not loaded'
            self.status_changed.emit()
            print(self.lasterror)
            return False
        if self.ChannelType != Channel_NotOpened:
            self.close()
        self.EQHandle = [0 for i in range(NumEQBands)]
        self.fftbands = [0 for i in range(NumFFTBands)]
        if 'http://' in fn or 'https://' in fn:
            self.Channel = self.libraries.load_url(fn)
            if self.Channel == 0:
                self.lasterror = f'URL not loaded! Error code: {BASS_ErrorGetCode()}'
                self.status_changed.emit()
                print(self.lasterror)
                return False
            self.ChannelType = Channel_Internet
        else:
            ext = fn[-4:].lower()
            if ext not in self.exts:
                self.lasterror = f'Format {ext} is not supported (see BASS libraries in app directory)'
                self.status_changed.emit()
                print(self.lasterror)
                return False
            binfn = fn.encode()
            self.Channel = self.libraries.load(binfn, ext)
            if self.Channel == 0:
                self.lasterror = 'File not loaded!'
                self.status_changed.emit()
                print(self.lasterror)
                return False
            self.ChannelType = Channel_Stream

        self.PlayerMode = PlayMode_Ready

        self.set_eqeffect(self.EqualizerEnabled)
        self.set_volume(self.volume)
        BASS_ChannelSetSync(self.Channel, BASS_SYNC_END, 0, self.onEndPlay, 0)
        self.status_changed.emit()
        self.currentfilename = fn
        return True

    def get_volume(self):
        return self.volume

    def set_volume(self, v):
        if v > 100:
            v = 100
        elif v < 0:
            v = 0
        self.volume = v
        if self.ChannelType == Channel_Stream or Channel_Internet:
            BASS_ChannelSetAttribute(self.Channel, BASS_ATTRIB_VOL, v/100)

            #return BASS_SetVolume(v/100)

    def play_pause(self):
        if self.ChannelType == Channel_NotOpened:
            return False
        if self.PlayerMode == PlayMode_Playing:
            self.pause()
        else:
            self.play()
        return True

    def play(self):
        if self.ChannelType == Channel_NotOpened: return
        if BASS_ChannelPlay(self.Channel, False):
            self.PlayerMode = PlayMode_Playing
            self.status_changed.emit()

    def stop(self):
        if self.ChannelType == Channel_NotOpened: return
        if self.PlayerMode == PlayMode_Playing or self.PlayerMode == PlayMode_Paused:
            BASS_ChannelStop(self.Channel)
            self.PlayerMode = PlayMode_Stopped
            if self.ChannelType == Channel_Stream:
                BASS_ChannelSetPosition(self.Channel, 0, BASS_POS_BYTE)
            self.status_changed.emit()

    def Restart(self):
        pass

    def pause(self):
        if self.ChannelType == Channel_NotOpened: return
        if BASS_ChannelPause(self.Channel):
            self.PlayerMode = PlayMode_Paused
            self.status_changed.emit()

    def close(self):
        if self.ChannelType == Channel_NotOpened: return
        if self.EqualizerEnabled:
            for i in range(len(self.EQHandle)):
                if self.EQHandle[i] != 0:
                    BASS_ChannelRemoveFX(self.Channel, self.EQHandle[i])
                    self.EQHandle[i] = 0
        BASS_StreamFree(self.Channel)
        self.Channel = 0
        self.ChannelType = Channel_NotOpened
        self.PlayerMode = PlayMode_Standby

    def set_position(self, pos): #sec
        if self.ChannelType == Channel_NotOpened: return
        if self.ChannelType == Channel_Stream:
            SongPos = BASS_ChannelSeconds2Bytes(self.Channel, pos)
            BASS_ChannelSetPosition(self.Channel, SongPos, BASS_POS_BYTE)

    def get_position(self):
        if self.ChannelType == Channel_NotOpened: return 0
        result = BASS_ChannelGetPosition(self.Channel, BASS_POS_BYTE)
        if result < 0: result = 0
        if result == 0: return 0
        return int(BASS_ChannelBytes2Seconds(self.Channel, result))

    #def getTimePos(self):
    #    if self.ChannelType == Channel_NotOpened: return '0.00'
    #    pos = self.get_position()
    #    return self.secondsToTime(pos)

    def get_length(self):
        if self.ChannelType != Channel_Stream: return 0
        result = BASS_ChannelGetLength(self.Channel, BASS_POS_BYTE)
        if result < 0: result = 0
        if result == 0: return 0
        return int(BASS_ChannelBytes2Seconds(self.Channel, result))

    #def getTimeDuration(self):
    #    if self.ChannelType == Channel_NotOpened: return '0.00'
    #    pos = self.get_length()
    #    return self.secondsToTime(pos)

    def update_eq_bands(self, bands):
        for i, b in enumerate(self.EQBands):
            b.CenterFreq = bands[i][0]
            b.Bandwidth = bands[i][1]
        if self.EqualizerEnabled:
            for i in range(len(self.EQHandle)):
                if self.EQHandle[i] == 0:
                    self.EQHandle[i] = BASS_ChannelSetFX(self.Channel, BASS_FX_DX8_PARAMEQ, 0)
                param = BASS_DX8_PARAMEQ()
                param.fGain = self.EQBands[i].Gain
                param.fBandwidth = self.EQBands[i].Bandwidth
                param.fCenter = self.EQBands[i].CenterFreq
                BASS_FXSetParameters(self.EQHandle[i], ctypes.pointer(param))

    def set_eqeffect(self, enabled):
        self.EqualizerEnabled = enabled
        if self.ChannelType == Channel_NotOpened:
            self.EQHandle = [0 for i in range(NumEQBands)]
            return False

        if enabled:
            for i in range(len(self.EQHandle)):
                if self.EQHandle[i] == 0:
                    self.EQHandle[i] = BASS_ChannelSetFX(self.Channel, BASS_FX_DX8_PARAMEQ, 0)
                param = BASS_DX8_PARAMEQ()
                param.fGain = self.EQBands[i].Gain
                param.fBandwidth = self.EQBands[i].Bandwidth
                param.fCenter = self.EQBands[i].CenterFreq
                BASS_FXSetParameters(self.EQHandle[i], ctypes.pointer(param))
        else:
            for i in range(len(self.EQHandle)):
                if self.EQHandle[i] != 0:
                    BASS_ChannelRemoveFX(self.Channel, self.EQHandle[i])
                    self.EQHandle[i] = 0

    def set_eqgain(self, index, gain):
        if gain < -15:
            gain = -15
        elif gain > 15:
            gain = 15
        self.EQBands[index].Gain = gain
        if self.ChannelType == Channel_NotOpened: return False
        if not self.EqualizerEnabled: return False
        if index < 0 or index > 9: return False
        if self.EQHandle[index] == 0: return False
        param = BASS_DX8_PARAMEQ()
        param.fGain = self.EQBands[index].Gain
        param.fBandwidth = self.EQBands[index].Bandwidth
        param.fCenter = self.EQBands[index].CenterFreq
        return BASS_FXSetParameters(self.EQHandle[index], ctypes.pointer(param))

    def decreasefft(self):
        self.zerofft = True
        for i in range(NumFFTBands):
            if self.fftbands[i] > 0:
                self.fftbands[i] -= 5
                if self.fftbands[i] < 1:
                    self.fftbands[i] = 0
                else:
                    self.zerofft = False

    def get_spec_data(self):
        if self.ChannelType == Channel_NotOpened or BASS_ChannelIsActive(self.Channel) != BASS_ACTIVE_PLAYING:
            return None
        data = self.tspecdata()
        fts = BASS_ChannelGetData(self.Channel, ctypes.pointer(data), self.spec_size)
        if fts == 0xffffffff:
            return None
        return data

    def get_fftdata(self, scale=30):
        if self.ChannelType == Channel_NotOpened:
            self.decreasefft()
            return False
        if BASS_ChannelIsActive(self.Channel) != BASS_ACTIVE_PLAYING:
            self.decreasefft()
            return False

        fftdata = self.tfftdata()
        fts = BASS_ChannelGetData(self.Channel, ctypes.pointer(fftdata), BASS_DATA_FFT2048)
        if fts == 0xffffffff:
            self.lasterror = 'can not get fftdata return ffffffff'
            self.decreasefft()
            return False
        self.zerofft = False

        scale_3 = 3 * scale
        for i in range(NumFFTBands):
            peak = 0
            for k in range(self.fft_limits[i][0], self.fft_limits[i][1]):
                if peak < fftdata[k]:
                    peak = fftdata[k]
            f = round(peak**0.5 * scale_3)
            # Decrease the value of fftBands[i] smoothly for better looking
            if f > self.fftbands[i]:
                  self.fftbands[i] = f
            else:
                if self.fftbands[i] >= 2:
                    self.fftbands[i] -= 2
                else:
                    self.fftbands[i] = 0
        return True

    def get_eqfreq(self):
        return [b.CenterFreq for b in self.EQBands]

    @SYNCPROC
    def onEndPlay(synhandle, buff, length, user):
        if player_instance != None:
            player_instance.stream_finished.emit()
        #BASS_ChannelSetSync(self.Channel, BASS_SYNC_END, 0, onEndPlay, 0)

    def get_meta(self):
        # if self.ChannelType == Channel_NotOpened:
        #    return None
        pass
