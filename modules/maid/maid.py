import random
import sys

from pyircsdk import Module


class MaidModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "maid")
        self.maids = [
            "cleans bedroom", 
            "cleans toilet", 
            "cleans laptop",
            "cleans table",
            "cleans dishes",
            "do nothing",
            "cleans whole apartment",
            "cleans living room",
            "cleans car",
            "washes underwears",
            "buys groceries",
            "makes coffee",
            "makes tea",
            "cleans bathroom",
            "walks the doggie",
            "does the laungry",
            "washes the shoes",
            "cleans bathtub"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                giveTo = command.args[0]
                maid = random.choice(self.maids)
                if command.args[0] in self.maids:
                    maid = command.args[0]
                    giveTo = command.args[1]
                    self.irc.privmsg(message.messageTo, "Yes, sir/ma'am, the maid %s for %s" % (maid, giveTo))
                    return
                
                self.irc.privmsg(message.messageTo, "Yes, sir/ma'am, the maid %s for %s" % (maid, giveTo))

    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "Sorry, the maid can't do it because you forgot to pay her salary T_T")
                return