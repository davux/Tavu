# -*- coding: utf-8 -*-
# vi: sts=4 et sw=4

"""Everything that is related to configuration file management."""

import app
from common import problem, debug
import ConfigParser
import os
import shutil
import sys

_defaultsFile = '/usr/share/%s/dotfile.skel' % app.identifier
_globalFile = '/etc/kde3/%src' % app.identifier
_userFile = os.path.expanduser('~/.kde/share/config/%src' % app.identifier)

def createUserConf(): #TODO: test
    """Create the user-level configuration file from the defaults file
    
    If the file already exists, do nothing. Otherwise, copy the defaults
    file to user level.
    """
    try:
        if not os.path.exists(_userFile):
            debug('Creating configuration file.')
            shutil.copyfile(_defaultsFile, _userFile)
    except (IOError, os.error), why:
        problem('Unable to create the configuration file: %s' % why, True)


#TODO: Use it at some point :p
def handleMissingSetting(section, keyName): #TODO: test
    """Handle when a configuration setting is missing. May return the
    value to use, if it makes sense.
    """
    if (section == 'Jabber'):
        if (keyName == 'jid'):
            problem('There is no configured JID. Please configure a JID and '
            'a password\nin your configuration file: %s' % _userFile, True)
        elif (keyName == 'password'):
            problem('There is no configured jabber password. Please configure '
                    'a JID and a password\nin your configuration file: '
                    '%s' % _userFile, True)
    else:
        debug("Returning empty value for %s in section [%s]" %
          (keyName, section), 1)

def dumpConfiguration(debuglvl = 0):
    debug("### Configuration ###", debuglvl)
    for section in config.sections():
        debug("[%s]" % section, debuglvl)
        for option in config.options(section):
            debug("%s = %s" % (option, config.get(section, option)), debuglvl)
        debug('', debuglvl)
    debug("#####################", debuglvl)
            
config = ConfigParser.SafeConfigParser()
debug('Reading configuration files', 1)
config.read([_globalFile, _userFile])
dumpConfiguration(7)
