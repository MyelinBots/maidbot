import random
import sys

from pyircsdk import Module


class CleanModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "clean")
        self.cleans = [
            "bedroom", 
            "toilet", 
            "laptop",
            "table",
            "dishes",
            "nothing",
            "apartment",
            "living room",
            "car"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                clean = random.choice(self.cleans)
                if command.args[0] in self.cleans:
                    clean = command.args[0]
                    giveTo = command.args[1]
                    self.irc.privmsg(message.messageTo, "The maid cleans %s for %s" % (clean, giveTo))
                    return
                
                self.irc.privmsg(message.messageTo, "The maid cleans %s for %s" % (clean, giveTo))

    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "The maid can't do it because you forgot to pay her salary T_T")
                return