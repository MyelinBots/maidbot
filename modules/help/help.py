import sys
import json

from pyircsdk import Module


class HelpModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "help")

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "Hello, %s, these are available commands; !cake, !coffee, !drink, !maid, !ramen, !food, !tea, !kiss, !hug, and !slap" % message.messageFrom)
                self.irc.privmsg(message.messageTo, "To play pigeon game; !shoot and to check score; !score")
                self.irc.privmsg(message.messageTo, "To check your daily horoscope; !hor <sign>")
                return
