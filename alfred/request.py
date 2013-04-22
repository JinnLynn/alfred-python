# -*- coding: utf-8 -*-

import os
import urllib, urllib2, urlparse
import Cookie
from cookielib import CookieJar
import base64

"""
Simple module to request HTTP

JinnLynn
http://jeeker.net

get(url, **kwargs)
post(url, **kwargs)
download(url, **kwargs)

Request(
    'http://jeeker.net',
    data = {},
    type = 'GET',               # GET POST default:GET
    referer = '',
    user_agent = '',
    cookie = None,              # CookieJar, Cookie.S*Cookie, dict, string
    auth = {'usr':'', 'pwd':''}, # Only Basic Authorization
    debug = False
    )
"""

_DEFAULT_TIMEOUT = 90

def get(url, **kwargs):
    kwargs.update(type='GET')
    return Request(url, **kwargs)

def post(url, **kwargs):
    kwargs.update(type='POST')
    return Request(url, **kwargs)

def download(url, local, **kwargs):
    if not local:
        raise ValueError('local filepath is empty')
    try:
        if not os.path.exists(os.path.dirname(local)):
            os.makedirs(os.path.dirname(local))
        res = Request(url, **kwargs)
        read_size = 0
        real_size = int(res.header['content-length'])
        with open(local, 'wb') as f:
            while True:
                block = res.response.read(1024*8)
                if not block:
                    break
                f.write(block)
                read_size += len(block)
        if read_size < real_size:
            raise urllib.ContentTooShortError(
                'retrieval incomplete: got only {} out of {} bytes'.formate(read_size, real_size),
                None
                )
    except Exception, e:
        raise e

class Request(object):
    def __init__(self, url, **kwargs):
        self.request = None
        self.response = None
        self.code = -1
        self.info = {}
        self.cookieJar = None
        self.reason = ''

        data = kwargs.get('data', None)
        if data:
            if isinstance(data, dict):
                data = urllib.urlencode(data)
            if not isinstance(data, basestring):
                data = None
                raise ValueError('data must be string or dict')

        request_type = kwargs.get('type', 'POST')
        if data and isinstance(request_type, basestring) and request_type.upper()!='POST':
            url = '{}?{}'.format(url, data)
            data = None # GET data must be None

        self.request = urllib2.Request(url, data)

        # referer
        referer = kwargs.get('referer', None)
        if referer:
            self.request.add_header('referer', referer)

        # user-agent
        user_agent = kwargs.get('user_agent', None)
        if user_agent:
            self.request.add_header('User-Agent', user_agent)

        # auth
        auth = kwargs.get('auth', None)
        if auth and isinstance(auth, dict) and auth.has_key('usr'):
            auth_string = base64.b64encode('{}:{}'.format(auth.get('usr',''), auth.get('pwd','')))
            self.request.add_header('Authorization', 'Basic {}'.format(auth_string))  

        # cookie
        cookie = kwargs.get('cookie', None)
        cj = None
        if cookie:
            if isinstance(cookie, CookieJar):
                cj = cookie
            elif isinstance(cookie, dict):
                result = []
                for k, v in cookie.iteritems():
                    result.append('{}={}'.format(k, v))
                cookie = '; '.join(result)
            elif isinstance(cookie, Cookie.BaseCookie):
                cookie = cookie.output(header='')
            if isinstance(cookie, basestring):
                self.request.add_header('Cookie', cookie)
        if cj is None:
            cj = CookieJar()

        #! TODO: proxy


        # build opener
        debuglevel = 1 if kwargs.get('debug', False) else 0
        opener = urllib2.build_opener(
            urllib2.HTTPHandler(debuglevel=debuglevel),
            urllib2.HTTPSHandler(debuglevel=debuglevel),
            urllib2.HTTPCookieProcessor(cj)
            )

        # timeout
        timeout = kwargs.get('timeout')
        if not isinstance(timeout, int):
            timeout = _DEFAULT_TIMEOUT

        try:
            self.response = opener.open(self.request, timeout=timeout)
            self.code = self.response.getcode()
            self.header = self.response.info().dict
            self.cookieJar = cj
        except urllib2.HTTPError, e:
            self.code = e.code
            self.reason = '{}'.format(e)
            raise e
        except urllib2.URLError, e:
            self.code = -1
            self.reason = e.reason
            raise e
        except Exception, e:
            self.code = -1
            self.reason = '{}'.format(e)
            raise e

    def isSuccess(self):
        return 200 <= self.code < 300

    def getContent(self):
        return self.response.read()