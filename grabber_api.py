# coding=utf-8
from youtube_dl.extractor import youtube
from thirdparty_grabber.youtube_dl.utils import ExtractorError

__author__ = 'gentoo'

from youtube_dl import YoutubeDL
import thirdparty_grabber
import traceback
import re
import myexceptions
from config import Config


class GrabberApi(object):
    """
    This is is a programming API for accessing youtube-dl functions
    """

    def __init__(self, url, ip=None, formats="22/18/35/34/6/5"):
        """
        
        :param url: String of the url
        :type url: str
        :param ip: Ip to use
        :type ip: str
        :return:
        """
        self.url = url
        self.parseResults = None
        self.formats = formats
        self.config = Config()

    def getVideoUrl(self):
        self._parse()

        return self.parseResults['url']

    def getVideoTitle(self):
        self._parse()

        return self.makeSecureTitle(self.parseResults['title'])

    def getVideoLength(self):
        self._parse()

        return self.parseResults['duration']

    def getFormatId(self):
        self._parse()

        return self.parseResults['format_id']

    def getVideoId(self):
        self._parse()

        return self.parseResults['id']

    def getExt(self):
        self._parse()

        return self.parseResults['ext']

    def makeSecureTitle(self, string):
        string = string.replace(u"Ü", u"Ue")\
            .replace(u"Ä", u"Ae")\
            .replace(u"Ö", u"Oe")\
            .replace(u"ü", u"ue")\
            .replace(u"ä", u"ae")\
            .replace(u"ö", u"oe")
        string = re.sub(r"[^\w \[\]\(\)-]", '', string)
        string = " ".join(string.split())

        return string

    def _parse(self):
        if self.parseResults is None:
            try:
                inst = YoutubeDL({
                    "outtmpl": "%(title)s-%(id)s.%(ext)s",
                    "skip_download": True,
                    "quiet": True,
                    #"format": self.formats,
                    "verbose": True
                })

                #self.parseResults = inst.download([self.url])['entries'][0]
                inst.get_info_extractor("Youtube")
                inst.get_info_extractor("Vimeo")
                self.parseResults = inst.extract_info(self.url, False)
            except thirdparty_grabber.youtube_dl.utils.DownloadError as e:
                if "This video does not exist" in e:
                    raise myexceptions.FetchingException("YouTube said: This video does not exist.", self.config.ERROR_404)
                if "GEMA" in e:
                    raise myexceptions.FetchingException("BANNED BY GEMA", self.config.ERROR_GEMA)

                raise myexceptions.FetchingException(e.message, self.config.ERROR_CUSTOMMESSAGE)

if __name__ == "__main__":
    #test = GrabberApi("http://vimeo.com/103389185")
    test = GrabberApi("https://www.youtube.com/watch?v=OsgUJcirboo")
    print(test.getVideoTitle())
    print(test.getVideoUrl())