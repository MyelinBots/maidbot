import sys
import json

from pyircsdk import Module


class HelpModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "halp")

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "Hello, %s, these are available commands; !cake, !coffee, !drink, !maid, !ramen, !food, !tea, !snack, !kiss, !hug, and !slap" % message.messageFrom)
                self.irc.privmsg(message.messageTo, "Check out the daily quotes; !quote")
                self.irc.privmsg(message.messageTo, "To check your daily horoscope; !hor <sign>")
                return
