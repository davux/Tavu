# -*- coding: utf-8 -*-
# vi: sts=4 et sw=4

import app
from common import problem, debug
from conf import config
from ConfigParser import NoOptionError, NoSectionError
import notifications
from pyxmpp.all import JID
from pyxmpp.jabber.client import JabberClient

class JabberBot(JabberClient):
    """Simple bot (client) example. Uses `pyxmpp.jabber.client.JabberClient`
    class as base. That class provides basic stream setup (including
    authentication) and Service Discovery server. It also does server address
    and port discovery based on the JID provided."""

    def __init__(self, jid, password):
        if not jid.resource:
            jid = JID(jid.node, jid.domain, app.name)
        JabberClient.__init__(self, jid, password)
        self.disco_info.add_feature("jabber:iq:version")

    def session_started(self):
        """This is called when the IM session is successfully started
        (after all the neccessery negotiations, authentication and
        authorizasion).
        That is the best place to setup various handlers for the stream.
        Do not forget about calling the session_started() method of the base
        class!"""
        self.request_roster()
        JabberClient.session_started(self)

    # Offline messages are retrieved before the roster is. Since our handling
    # of incoming messages needs the roster, we request it ASAP.
    def authorized(self):
        JabberClient.authorized(self)

    def roster_updated(self):
        self.stream.set_message_handler("normal", self.message)

    def get_version(self,iq):
        """Handler for jabber:iq:version queries.

        jabber:iq:version queries are not supported directly by PyXMPP, so the
        XML node is accessed directly through the libxml2 API.  This should be
        used very carefully!"""
        iq=iq.make_result_response()
        q=iq.new_query("jabber:iq:version")
        q.newTextChild(q.ns(),"name", app.description)
        q.newTextChild(q.ns(),"version", app.version)
        self.stream.send(iq)
        return True

    def message(self,stanza):
        """Message handler for the component.

        Create a human-readable text from the message information, and
        trigger a DBus notification containing the text.

        :returns: `True` to indicate that the stanza should not be processed
        any further."""
        #TODO: Extract xhtml version as well if possible
        body = stanza.get_body()
        debug('Message received', 2)
        if not body:
            return False
        if not self.acceptMessage(stanza):
            debug('Refused.', 4)
            return False
        subject = stanza.get_subject()
        f = stanza.get_from()
        (text, appName, summary) = notifications.message2text(body,
                   self.jid2nick(f), f.resource, f.bare().as_unicode(), subject)
        notifications.notify(text, appName, summary)
        return True

    def acceptMessage(self, stanza):
        """Tell if the message is accepted or not."""
        section = 'Message filters'
        sender = stanza.get_from().bare()
        try:
            crit = config.get(section, 'accept')
        except (NoOptionError, NoSectionError):
            crit = 'roster+self'
        debug("Critere: %s" % crit, 8);
        if crit == 'all':
            return True
        if crit == 'none':
            return False
        if crit in ['self', 'roster+self']:
            if sender == self.jid.bare():
                return True
        if crit in ['list', 'roster+list']:
            try:
                list = config.get(section, 'list').split(', ')
            except (NoOptionError, NoSectionError):
                list = []
            if sender.as_utf8() in list:
                return True
        if crit in ['roster', 'roster+list', 'roster+self']:
            try:
                self.roster.get_item_by_jid(sender)
                return True
            except KeyError:
                return False
        return False

    def jid2nick(self, jid):
        """Look for the nick of the given JID in the roster.
        
        If the JID exists in the roster, translate it into the
        associated name.

        :returns: The name associated to the JID if it exists in the roster,
        the JID unchanged otherwise."""
        try:
            name = self.roster.get_item_by_jid(jid.bare()).name
        except KeyError:
            name = jid.as_unicode()
        return name
