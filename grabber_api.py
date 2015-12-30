# coding=utf-8
from __future__ import unicode_literals
from thirdparty_grabber.youtube_dl.extractor.soundcloud import SoundcloudIE
from thirdparty_grabber.youtube_dl.extractor.vimeo import VimeoIE
from thirdparty_grabber.youtube_dl.extractor.youtube import YoutubeIE
from thirdparty_grabber.youtube_dl.utils import ExtractorError
from youtube_dl import YoutubeDL
import thirdparty_grabber
import re
import myexceptions
from config import Config
import random


class GrabberApi(object):
    """
    This is is a programming API for accessing youtube-dl functions
    """

    supported_ies_re = {}

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
        self.portal = ""
        self.inst = YoutubeDL({
                    "outtmpl": "%(title)s-%(id)s.%(ext)s",
                    "skip_download": True,
                    "quiet": True,
                    "cachedir": False,
                    #"format": self.formats,
                    "verbose": False
                })

                #self.parseResults = inst.download([self.url])['entries'][0]
        self.supported_ies_re["youtube"] = self.inst.get_info_extractor("Youtube")
        self.supported_ies_re["vimeo"] = self.inst.get_info_extractor("Vimeo")
        self.supported_ies_re["soundcloud"] = self.inst.get_info_extractor("Soundcloud")

        if not self.supported():
            raise myexceptions.FetchingException("This Platform is not supported", self.config.ERROR_UNKNOWN_PORTAL)

    def supported(self):
        for key in self.supported_ies_re:
            ie = self.supported_ies_re[key]
            if re.search(ie._VALID_URL, self.url) is not None:
                self.portal = key
                return True
        return False

    def get_portal(self):
        return self.portal

    def get_video_url(self):
        self._parse()

        print self.parseResults

        return self.parseResults['url']

    def get_video_url_by_format(self, desired_format):
        self._parse()

        if desired_format == "mp4":
            return self.get_video_url()

        if self.parseResults["extractor"] == "youtube" and "formats" in self.parseResults:
            for avail_formats in self.parseResults['formats']:
                print avail_formats
                if desired_format.lower() == avail_formats['ext']:
                    print avail_formats
                    return avail_formats['url']

        return self.get_video_url()

    def get_video_title(self):
        self._parse()

        return self.make_secure_title(self.parseResults['title'])

    def get_video_length(self):
        self._parse()
        if "duration" not in self.parseResults:
            return 1

        return self.parseResults['duration']

    def get_format_id(self):
        self._parse()

        return self.parseResults['format_id']

    def get_video_id(self):
        self._parse()

        return self.parseResults['id']

    def get_ext(self):
        self._parse()

        return self.parseResults['ext']

    def make_secure_title(self, string):
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
        # self.parseResults = {
        #     'url': 'http://localhost/video.ogg',
        #     'title': str(random.randint(0, 10000000000000)),
        #     'duration': 1000,
        #     'format_id': 22,
        #     'id': random.choice([10,11,12,13,14]),
        #     'ext': 'mp4'
        # }
        if self.parseResults is None:
            try:

                self.parseResults = self.inst.extract_info(self.url, False)
            except thirdparty_grabber.youtube_dl.utils.DownloadError as e:
                if "This video does not exist" in e:
                    raise myexceptions.FetchingException("YouTube said: This video does not exist.", self.config.ERROR_404)
                if "GEMA" in e:
                    raise myexceptions.FetchingException("BANNED BY GEMA", self.config.ERROR_GEMA)

                raise myexceptions.FetchingException(e.message, self.config.ERROR_CUSTOMMESSAGE)

if __name__ == "__main__":
    test = GrabberApi("http://vimeo.com/103389185")
    test = GrabberApi("https://www.youtube.com/watch?v=ufbHbmygwp8")
    test = GrabberApi("https://vimeo.com/140447838")
    test = GrabberApi("https://soundcloud.com/travisscott-2/travis-scott-antidote")
    print(test.get_portal())
    print(test.get_video_title())
    print(test.get_video_url())
    # print(test.get_video_url_by_format('aac'))
