# -*- coding: utf-8 -*-
import os, sys, plistlib, time

from feedback import Feedback

__bundle_id__ = None
__config_folder__ = os.path.expanduser('~/Library/Application Support/Alfred 2/Workflow Data/')
__cache_folder__ = os.path.expanduser('~/Library/Caches/com.runningwithcrayons.Alfred-2/Workflow Data/')

def bundleID():
    global __bundle_id__
    if __bundle_id__:
        return __bundle_id__
    path = os.path.abspath('./info.plist')
    try:
        info = plistlib.readPlist(path)
        __bundle_id__ = info['bundleid']
    except Exception, e:
        raise Exception('get Bundle ID fail. {}'.format(e))
    return __bundle_id__

def log(s):
    log_text = '[{} {}]: {}\n'.format(bundleID(), time.strftime('%Y-%m-%d %H:%M:%S'), s)
    log_file = os.path.abspath('./log.txt')
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write(log_text)
    else:
        with open(log_file, 'a') as f:
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
    except Exception, e:
        log('Notification failed. {}'.format(e))
    