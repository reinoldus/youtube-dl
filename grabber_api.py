__author__ = 'gentoo'

from youtube_dl import YoutubeDL
import thirdparty_grabber
import traceback
import myexceptions

import functools
import httplib
import urllib2

class BoundHTTPHandler(urllib2.HTTPHandler):

    def __init__(self, source_address=None, debuglevel=0):
        urllib2.HTTPHandler.__init__(self, debuglevel)
        self.http_class = functools.partial(httplib.HTTPConnection,
                source_address=source_address)

    def http_open(self, req):
        return self.do_open(self.http_class, req)

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
        handler = BoundHTTPHandler(source_address=('192.168.1.10', 0))
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

    def getVideoUrl(self):
        self._parse()

        return self.parseResults['url']

    def getVideoTitle(self):
        self._parse()

        return self.parseResults['title']

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

    def _parse(self):
        if self.parseResults is None:
            try:
                inst = YoutubeDL({
                    "outtmpl": "%(title)s-%(id)s.%(ext)s",
                    "skip_download": True,
                    "quiet": True,
                    "format": self.formats
                })

                self.parseResults = inst.download([self.url])['entries'][0]
            except thirdparty_grabber.youtube_dl.utils.DownloadError as e:
                if "This video does not exist" in e:
                    raise myexceptions.FetchingException("YouTube said: This video does not exist.", 511)
                elif "GEMA" in e:
                    raise myexceptions.FetchingException("YouTube said: This video does not exist.", 514)
