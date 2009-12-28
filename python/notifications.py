# -*- coding: utf-8 -*-
# vi: sts=4 et sw=4

import app
from common import problem, debug
from conf import config
from globalvars import encoding
import dbus
import sys
from string import Template

def notify(text, appName, eventName):
    "Trigger a notification with the given text using KNotify."
    # We convert from unicode to isolatin9 instead of the system
    # encoding to workaround a bug in PyDCOP (see
    # http://bugs.kde.org/show_bug.cgi?id=105084), unless there's no
    # corresponding iso-8859-15 chararacter.
    try: text = text.encode('iso-8859-15')
    except UnicodeEncodeError:
        try: text = text.encode(encoding)
        except: text = '[<b>Error:</b> Unable to decode text]'
    try: appName = appName.encode('iso-8859-15')
    except UnicodeEncodeError: appName = app.identifier
    try: eventName = eventName.encode('iso-8859-15')
    except UnicodeEncodeError: eventName = '' #XXX: Better fallback name?
    try:
	session_bus = dbus.SessionBus()
	obj = session_bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
	interface = dbus.Interface(obj, 'org.freedesktop.Notifications')
	interface.Notify(appName, 0, '', eventName, text, [], {}, 16000)
    except:
        problem('Could not trigger notification: %s \n' % sys.exc_info()[1])

def message2text(body, fromName, resource, fromAddr, subject):
    """
    Return a triplet from the body + sender + subject
    - the first element is the text of the notification
    - the second element is the application name
    - the third element is the event name
    """
    if fromName == None:
        fromName = fromAddr
    section = 'Event information'
    try: text_format = config.get(section, 'text')
    except: text_format = '$body'
    try: appName_format = config.get(section, 'app name')
    except: appName_format = '$senderresource'
    try: eventName_format = config.get(section, 'event name')
    except: eventName_format = '$subject'
    subst = {'body': body, 'senderjid': fromAddr, 'subject': subject,
             'sender': fromName, 'senderresource': resource}
    text_tmpl = Template(text_format)
    appName_tmpl = Template(appName_format)
    eventName_tmpl = Template(eventName_format)
    return (text_tmpl.safe_substitute(subst),
            appName_tmpl.safe_substitute(subst),
            eventName_tmpl.safe_substitute(subst))
