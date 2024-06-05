import sys
import json

from pyircsdk import Module


class GreetingModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "", "")

    def handleCommand(self, message, command):

        if message.command == 'JOIN' and message.messageFrom != self.irc.config.nick:            
            self.irc.privmsg(message.trailing, "Hello, %s, welcome to %s, enjoy your stay :)" % (message.messageTo, message.messageFrom))
