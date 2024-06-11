import random
import sys

from pyircsdk import Module


class HugModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "hug")
        self.hugs = [
            "tightly 🤗",
            "warmly 🤗",
            "in celebration 🎉🤗",
            "gratefully 🤗",
            "with a big smile 😊🤗",
            "tightly 🤗",
            "with love ❤️🤗",
            "with joy 🥳🤗",
            "tightly for support 🤗",
            "proudly 🌟🤗",
            "happily 😂🤗"
        ]

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                if len(command.args) == 0:
                    hug = random.choice(self.hugs)
                    self.irc.privmsg(message.messageTo, "hugs %s %s" % (message.messageFrom, hug))
                    return

                giveTo = command.args[0]
                hug = random.choice(self.hugs)
                self.irc.privmsg(message.messageTo, "hugs %s %s" % (giveTo, hug))
                
    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "Who do you want to hug?")
                return 

  
                
















                
