import sys
import json

from pyircsdk import Module


class HelpModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "help")

    def handleCommand(self, message, command):
        if message.command == self.fantasy + self.command:            
            self.irc.privmsg(message.trailing, "Hello, %s, these are available commands; !cake <nick> !drink <nick> !maid <nick> !ramen <nick> !snack <nick> !tea <nick>" % message.messageFrom)
            self.irc.privmsg(message.trailing, "To play pigeon game; !shoot and to check score; !score")

