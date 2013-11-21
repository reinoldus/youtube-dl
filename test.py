__author__ = 'gentoo'

from youtube_dl import YoutubeDL
test = YoutubeDL({
    "outtmpl": "%(title)s-%(id)s.%(ext)s",
    "skip_download": True,
    "quiet": True
})

print test.download(['http://m.youtube.com/watch?v=g71KpxVK1cg'])