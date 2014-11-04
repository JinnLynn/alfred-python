# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
import os, sys, subprocess, codecs
import plistlib
import json
from datetime import datetime
import unicodedata
import traceback

from .feedback import Feedback, Item
from . import __version__

_bundle_id = None
_config_base_dir = os.path.expanduser('~/Library/Application Support/Alfred 2/Workflow Data/')
_cache_base_dir = os.path.expanduser('~/Library/Caches/com.runningwithcrayons.Alfred-2/Workflow Data/')
_log_base_dir = os.path.expanduser('~/Library/Logs/Alfred 2')
_storage_base_dir = '/tmp/Alfred 2'

PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3

def bundleID():
    global _bundle_id
    if not _bundle_id:
        try:
            plist_path = os.path.abspath('./info.plist')
            prefs = plistlib.readPlist(plist_path)
            _bundle_id = prefs['bundleid'].strip()
            if not _bundle_id:
                raise ValueError('bundle id missing.')
        except:
            raiseWithFeedback()
    return _bundle_id

def setDefaultEncodingUTF8():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    del sys.setdefaultencoding

def getWorkflows():
    from .cache import cached
    @cached('workflows-alfred-python-v{}'.format(__version__), _expire=10)
    def _getWorkflows():
        workflows = {
            'enabled'   : {},
            'disabled'  : {},
            'bundleid_missing' : []
        }
        pref_file = os.path.expanduser('~/Library/Preferences/com.runningwithcrayons.Alfred-Preferences.plist')
        workflows_path = os.path.expanduser('~/Library/Application Support/Alfred 2/Alfred.alfredpreferences/workflows')
        try:
            # binary
            res = subprocess.check_output(['plutil', '-convert', 'json', '-o', '-', pref_file])
            pref = json.loads(res)
            if int(pref['version'].split('.')[0]) < 2:
                return workflows
        except:
            return workflows
        if pref.has_key('syncfolder'):
            syncfolder = os.path.expanduser(pref['syncfolder'])
            workflows_path = os.path.join(syncfolder, 'Alfred.alfredpreferences/workflows')
        if not os.path.isdir(workflows_path):
            return workflows
        for f in os.listdir(workflows_path):
            fullpath = os.path.join(workflows_path, f)
            if not os.path.isdir(fullpath):
                continue
            try:
                prefs = plistlib.readPlist(os.path.join(fullpath, 'info.plist'))
                bundleid = prefs['bundleid'].strip()
                if not bundleid:
                    workflows['bundleid_missing'].append(fullpath)
                    continue
                if prefs['disabled']:
                    workflows['disabled'].update({bundleid:fullpath})
                    continue
                workflows['enabled'].update({bundleid:fullpath})
            except Exception, e:
                pass
        return workflows

    return _getWorkflows()

def isWorkflowWorking(bundle_id):
    try:
        return bundle_id in getWorkflows().get('enabled', {}).keys()
    except:
        return False

def decode(s):
    return unicodedata.normalize("NFC", s.decode("utf-8"))

def log(s):
    log_dir = os.path.join(_log_base_dir, bundleID())
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    now = datetime.now()
    log_file = os.path.join(log_dir, '{}.log'.format(now.strftime('%Y-%m-%d')))
    log_text = '{}: {}\n'.format(now.strftime('%Y-%m-%d %H:%M:%S.%f'), s)
    with codecs.open(log_file, 'a', 'utf-8') as f:
        f.write(log_text)

def argv(pos, default=None):
    try:
        arg = sys.argv[pos]
    except:
        return default
    return arg

def exitWithFeedback(**kwargs):
    retcode = kwargs.pop('retcode', 0)
    fb = Feedback()
    fb.addItem(**kwargs)
    fb.output()
    sys.exit(retcode)

def exit(msg='', retcode=0):
    if msg:
        print(msg)
    sys.exit(retcode)
    
def query(word):
    scpt = 'tell application "Alfred 2" to search "{}"'.format(word)
    subprocess.call(['osascript', '-e', scpt])

def notify(title, subtitle, text='', sound=True):
    try:
        import objc, AppKit
        app = AppKit.NSApplication.sharedApplication()
        NSUserNotification = objc.lookUpClass("NSUserNotification")
        NSUserNotificationCenter = objc.lookUpClass("NSUserNotificationCenter")
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(title)
        notification.setSubtitle_(subtitle)
        notification.setInformativeText_(text)
        if sound:
            notification.setSoundName_("NSUserNotificationDefaultSoundName")
        NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)
    except Exception as e:
        log('Notification failed. {}'.format(e))

# ONLY used in 'try...except...'
def raiseWithFeedback(feedback=None):
    exc = traceback.format_exc()
    if not exc or len(exc.split('\n')) < 4:
        return
    excs = [s.strip() for s in exc.split('\n')]
    item = Item(title=excs[3], subtitle=(': ').join(excs[1:3]), valid=False)
    if not isinstance(feedback, Feedback):
        exitWithFeedback(item=item)
    feedback.addItem(item=item)
    feedback.output()
    exit()