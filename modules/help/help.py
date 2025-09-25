import random
import sys

from pyircsdk import Module

class HelpModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "halp")

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(
                    message.messageTo,
                    "Hello, %s, I am the Maid of DarkWorld Network. These are available commands:"
                    % message.messageFrom
                )
                self.irc.privmsg(message.messageTo, "Service: !cake, !coffee, !drink, !maid, !ramen, !food, !tea, !snack")
                self.irc.privmsg(message.messageTo, "Fun: !kiss, !hug, !slap")
                self.irc.privmsg(message.messageTo, "Info: !quote <nick>, !hor <sign> (horoscope), !w <location> (weather)")
                self.irc.privmsg(message.messageTo, "Utility: !invite maid <#channel>, !youtube <query>, !google <query>")
                self.irc.privmsg(message.messageTo, "Check all commands; !halp")
                self.irc.privmsg(message.messageTo, "✨ ~Thank you and enjoy your day!~ ✨😊")
                return






