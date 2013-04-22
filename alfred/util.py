# -*- coding: utf-8 -*-

import hashlib, random

import core

hashDigest = lambda s: hashlib.md5(s).hexdigest()

uid = lambda: hashDigest('{}'.format(random.getrandbits(25)))