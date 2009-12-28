# -*- coding: utf-8 -*-
# vi: sts=4 et sw=4

"""Common functions."""

import app
import sys

#TODO: Use notifications or something else, alternatively
def problem(desc = 'A problem occurred.', fatal = False, errorcode = 1):
    sys.stderr.write(desc + '\n')
    if fatal: sys.exit(errorcode)


#TODO: Refine the debugging
def debug(message, precise=0):
    if (precise <= app.max_verbosity):
        sys.stderr.write("%s[%s]: %s\n" % (app.identifier, precise, message))
