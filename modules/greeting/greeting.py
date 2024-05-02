import sys

from pyircsdk import Module


class GreetingModule(Module):
    def __init__(self, irc):
        super().__init__(irc, "", "hello")

    def handleCommand(self, message, command):
        if message.command == 'JOIN' and message.messageFrom != None and message.messageFrom != "Maid":
            
            self.irc.privmsg(message.trailing, "Hello, %s, welcome to the channel, enjoy your stay :)" % message.messageFrom)



