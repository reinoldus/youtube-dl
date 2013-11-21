__author__ = 'gentoo'

from youtube_dl import YoutubeDL


class GrabberApi(object):
    """
    This is is a programming API for accessing youtube-dl functions
    """

    def __init__(self, url):
        """
        
        :param url: String of the url
        :type url: str
        :return:
        """
        self.url = url
        self.parseResults = None

    def getParsedUrl(self):
        self._parse()

        return self.parseResults['url']

    def getTitle(self):
        self._parse()

        return self.parseResults['title']

    def getDuration(self):
        self._parse()

        return self.parseResults['duration']

    def getFormatId(self):
        self._parse()

        return self.parseResults['format_id']

    def getExt(self):
        self._parse()

        return self.parseResults['ext']

    def _parse(self):
        if self.parseResults is None:
            inst = YoutubeDL({
                "outtmpl": "%(title)s-%(id)s.%(ext)s",
                "skip_download": True,
                "quiet": True
            })

            self.parseResults = inst.download(self.url)['entries'][0]
