#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__  = (
    'Ricardo Garcia Gonzalez',
    'Danny Colligan',
    'Benjamin Johnson',
    'Vasyl\' Vavrychuk',
    'Witold Baryluk',
    'Paweł Paprota',
    'Gergely Imreh',
    'Rogério Brito',
    'Philipp Hagemeister',
    'Sören Schulze',
    'Kevin Ngo',
    'Ori Avtalion',
    'shizeeg',
    'Filippo Valsorda',
    'Christian Albrecht',
    'Dave Vasilevsky',
    'Jaime Marquínez Ferrándiz',
    'Jeff Crouse',
    'Osama Khalid',
    'Michael Walter',
    'M. Yasoob Ullah Khalid',
    'Julien Fraichard',
    'Johny Mo Swag',
    'Axel Noack',
    'Albert Kim',
    'Pierre Rudloff',
    'Huarong Huo',
    'Ismael Mejía',
    'Steffan \'Ruirize\' James',
    'Andras Elso',
    'Jelle van der Waa',
    'Marcin Cieślak',
    'Anton Larionov',
)

__license__ = 'Public Domain'

from .update import update_self
from .version import __version__
from .FileDownloader import (
    FileDownloader,
)
from .extractor import gen_extractors
from .YoutubeDL import YoutubeDL
from .PostProcessor import (
    FFmpegMetadataPP,
    FFmpegVideoConvertor,
    FFmpegExtractAudioPP,
    FFmpegEmbedSubtitlePP,
)

