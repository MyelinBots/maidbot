import sys
import json

from pyircsdk import Module


class GreetingModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "", "")

    def handleCommand(self, message, command):

        if message.command == 'JOIN' and message.messageFrom != self.irc.config.nick:            
            self.irc.privmsg(message.trailing, "Hello, %s, welcome to the channel, enjoy your stay :)" % message.messageFrom)
            self.irc.privmsg(message.trailing, "These are available commands; !cake <nick> !clean <nick> !drink <nick> !ramen <nick> !snack <nick> !tea <nick>")
