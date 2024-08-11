
import os
from pyircsdk import Module

from modules.horoscope.horoscope_api.horoscope_api import Horoscope


class HoroscopeModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "!", "hor")
        cacheTTL = os.getenv("HOROSCOPE_CACHE", 300)
        self.horoscope = Horoscope(cacheTTL)

    def handleCommand(self, message, command):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                if len(command.args) == 0:
                    self.irc.privmsg(message.messageTo, "Please share with me your sign")
                    return
                sign = command.args[0]
                message = self.horoscope.get_horoscope(sign=sign)
                self.irc.privmsg(message.messageTo, message)

    def handleError(self, message, command, error):
        if message.command == "PRIVMSG":
            if command.command == self.fantasy + self.command:
                self.irc.privmsg(message.messageTo, "Unfortunately, something went wrong, please try again")
                return  

