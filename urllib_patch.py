__author__ = 'ubuntu'

import httplib
import functools
import config
from random import choice
from urllib2 import AbstractHTTPHandler

myConfig = config.Config()

class HTTPSHandler(AbstractHTTPHandler):

    def https_open(self, req):
        ip = choice(myConfig.realIps)

        http_class = functools.partial(httplib.HTTPSConnection,
                        source_address=(ip, 0))
        return self.do_open(http_class, req)

    https_request = AbstractHTTPHandler.do_request_