# -*- coding: utf-8 -*-
import os, json, time, shutil, codecs
import hashlib

import core
from core import __cache_folder__

# { 'expire_time' : 0, data' : {} }

CACHE_DEFAULT_EXPIRE = 60 * 60 * 24

class Cache(object):
    def __init__(self):
        self.cache_dir = os.path.join(__cache_folder__, core.bundleID())
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def getFilepath(self, name):
        # convert to md5, more safe for file name
        name = hashlib.md5(name).hexdigest()
        return os.path.join(self.cache_dir, '{}.json'.format(name))

    def getContent(self, name):
        try:
            path = self.getFilepath(name)
            with codecs.open(path, 'r', 'utf-8') as f:
                return json.load(f)
        except:
            pass
    
    def get(self, name):
        try:
            cache = self.getContent(name)
            if cache['expire_time'] >= time.time():
                return cache['data']
        except:
            pass
        self.delete(name)
        
    def set(self, name, data, expire=CACHE_DEFAULT_EXPIRE):
        path = self.getFilepath(name)
        try:
            cache = {
                    'expire_time'   : time.time() + expire,
                    'data'          : data
                }
            with codecs.open(path, 'w', 'utf-8') as f:
                json.dump(cache, f, indent=4)
        except:
            pass

    def delete(self, name):
        path = self.getFilepath(name)
        if os.path.exists(path):
            os.remove(path)

    def clean(self):
        shutil.rmtree(self.cache_dir)

    def expireTimeout(self, name):
        try:
            cache = self.getContent(name)
            if cache['expire_time'] >= time.time():
                return cache['expire_time'] - time.time()
        except:
            pass
        return -1