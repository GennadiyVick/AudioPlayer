from mutagen.mp3 import MP3
# from mutagen.aac import AAC
from mutagen.mp4 import MP4

utf = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя'
lat = 'ÀÁÂÃÄÅšÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÜÛÚÝÞßàáâãäåžæçèéêëìíîïðñòóôõö÷øùüûúýþÿ'


def latin_conv(s):
    r = ''
    for i in range(len(s)):
        j = lat.find(s[i])
        r += utf[j] if j >= 0 else s[i]
    return r


class Metadata:
    def __init__(self):
        self.title = ''
        self.album = ''
        self.artist = ''
        self.date = ''
        self.genre = ''
        self.image = None
        self.info = None
        self.freq = 0
        self.bit = 0

    def get_tag(self, tag):
        t = self.info.get(tag)
        result = ''
        if t is None:
            return result
        if hasattr(t, 'text'):
            text = t.text
            if type(text) is list:
                text = text[0]
            if len(text) > 0:
                if hasattr(t, 'encoding'):
                    if str(t.encoding) == 'Encoding.LATIN1':
                        text = latin_conv(text)
            result = text
        else:
            result = str(t)
        return result


def get_mp4_tag(audio, tag, default: str | None = ""):
    result = audio.get(tag, [])
    if len(result) > 0:
        return result[0]
    return default


class MP3Data(Metadata):
    def __init__(self, filename, ext, with_cover=False):
        super(MP3Data, self).__init__()
        if ext == '.mp3':
            self.info = MP3(filename)
            self.bit = self.info.info.bitrate
            self.freq = self.info.info.sample_rate
            self.album = self.get_tag('TALB')
            self.title = self.get_tag('TIT2')
            if len(self.title) < 2:
                self.title = self.get_tag('TIT1')
            self.artist = self.get_tag('TPE1')
            self.genre = self.get_tag('TCON')
            if with_cover:
                for key in self.info:
                    if 'APIC' in key:
                        self.image = self.info.get(key).data
                        break
        elif ext == '.m4a' or ext == 'mp4':
            audio = MP4(filename)
            self.title = get_mp4_tag(audio, "\xa9nam")
            self.artist = get_mp4_tag(audio, "\xa9ART")
            self.album = get_mp4_tag(audio, "\xa9alb")
            self.genre = get_mp4_tag(audio, "\xa9gen")
            self.bit = audio.info.bitrate
            self.freq = audio.info.sample_rate
            if with_cover:
                self.image = get_mp4_tag(audio, 'covr', default=None)