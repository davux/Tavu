# -*- coding: utf-8 -*-
# vi: sts=4 et sw=4

"""Cross-module global variable definitions.
- encoding
"""

import locale

# XMPP protocol is Unicode-based to properly display data received
# _must_ convert it to local encoding or UnicodeException may be raised
locale.setlocale(locale.LC_CTYPE,"")
encoding=locale.getlocale()[1]
if not encoding:
    encoding="us-ascii"
