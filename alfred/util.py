# -*- coding: utf-8 -*-

import hashlib, random

hashDigest = lambda s: hashlib.md5(s).hexdigest()

uid = lambda: random.getrandbits(25)