# -*- coding: utf-8 -*-

"""
Alfred Python
A simple python module for alfred workflow。

Jian Lin
http://jeeker.net
The MIT License
"""

__version__     = '0.1'
__author__      = 'Jian Lin <eatfishlin@gmail.com>'
__license__     = 'MIT license'
__copyright__   = 'Copyright 2013 Jian Lin'

from .core import *
from .feedback import Feedback, Item
import cache
import config