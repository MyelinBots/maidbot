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
                    "Hello, %s, I am the Maid of DarkWorld Network. These are available commands; !cake, !coffee, !drink, !maid, !ramen, !food, !tea, !snack, !kiss, !hug, and !slap"
                    % message.messageFrom
                )
                self.irc.privmsg(message.messageTo, "→ Check out the daily quotes; !quote")
                self.irc.privmsg(message.messageTo, "→ To check your daily horoscope; !hor <sign>")
                self.irc.privmsg(message.messageTo, "→ To check the weather; !w <location>")
                self.irc.privmsg(message.messageTo, "→ To invite me to your channel; !invite maid <#channel>")
                self.irc.privmsg(message.messageTo, "→ To search YouTube; !youtube <query>")
                self.irc.privmsg(message.messageTo, "→ To search Google; !google <query>")
                self.irc.privmsg(message.messageTo, "→ To get help; !halp")
                self.irc.privmsg(message.messageTo, "✨ ~Thank you and enjoy your day!~ ✨😊")
                return
